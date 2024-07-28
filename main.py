import requests
from bs4 import BeautifulSoup
import os


# Function to create a directory if it does not exist
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Base URL and directory setup
base_url = "https://www.bailii.org"
cases_base_url = "/ie/cases/IESC/"
download_dir = "cases"
create_directory(download_dir)

# Years to scrape
years = [2024, 2023, 2022, 2021, 2020]


# Function to get all case links for a given year
def get_case_links(year):
    year_url = f"{base_url}{cases_base_url}{year}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(year_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {year_url} with status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    case_links = []

    # Extract all links within the ul tags
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag and 'Printable PDF version' not in a_tag.text:
                case_links.append(a_tag['href'])

    return case_links


# Function to download PDF from case link
def download_pdf(case_url, year):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(case_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {case_url} with status code {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_link = soup.find('a', string="Printable PDF version")

    if pdf_link:
        pdf_url = base_url + pdf_link['href']
        pdf_response = requests.get(pdf_url, headers=headers)

        if pdf_response.status_code == 200:
            pdf_name = pdf_url.split('/')[-1]
            year_path = os.path.join(download_dir, str(year))
            create_directory(year_path)
            pdf_path = os.path.join(year_path, pdf_name)

            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            print(f"Downloaded: {pdf_path}")
        else:
            print(f"Failed to download PDF: {pdf_url} with status code {pdf_response.status_code}")
    else:
        print(f"No PDF link found for {case_url}")


# Main script to iterate over each year and download PDFs
for year in years:
    print(f"Processing year: {year}")
    case_links = get_case_links(year)

    for case_link in case_links:
        full_case_url = base_url + case_link
        download_pdf(full_case_url, year)
