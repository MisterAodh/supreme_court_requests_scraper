import os
from PyPDF2 import PdfReader
import re
import json


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def split_text_into_paragraphs(text):
    # Split based on numbering scheme like 1., 2., 3., etc.
    paragraphs = re.split(r'(?<=\n)(\d+\.\s)', text)
    merged_paragraphs = []
    for i in range(0, len(paragraphs), 2):
        if i + 1 < len(paragraphs):
            merged_paragraphs.append(paragraphs[i] + paragraphs[i + 1])
        else:
            merged_paragraphs.append(paragraphs[i])
    return [p.strip() for p in merged_paragraphs if p.strip()]


def split_paragraphs_into_sentences(paragraphs):
    paragraphs_sentences = {}
    for i, paragraph in enumerate(paragraphs):
        sentences = [sentence.strip() for sentence in re.split(r'(?<=[.!?]) +', paragraph) if sentence.strip()]
        paragraphs_sentences[f"paragraph_{i}"] = sentences
    return paragraphs_sentences


def process_pdf_directory(base_directory):
    data = {}
    for year_dir in os.listdir(base_directory):
        year_path = os.path.join(base_directory, year_dir)
        if os.path.isdir(year_path):
            for pdf_file in os.listdir(year_path):
                if pdf_file.endswith(".pdf"):
                    pdf_path = os.path.join(year_path, pdf_file)
                    case_name = os.path.splitext(pdf_file)[0]
                    year_of_case = re.search(r'\d{4}', case_name).group()
                    case_key = f"{case_name}_{year_of_case}"

                    text = extract_text_from_pdf(pdf_path)
                    paragraphs = split_text_into_paragraphs(text)
                    paragraphs_sentences = split_paragraphs_into_sentences(paragraphs)

                    data[case_key] = paragraphs_sentences

    return data


# Base directory containing the cases directory
base_directory = "cases"

# Process the directory and get the data
data = process_pdf_directory(base_directory)

# Save the data to a JSON file
output_path = "cases_data.json"
with open(output_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data has been saved to {output_path}")
