import os
from datetime import datetime

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_file_structure(base_dir, years):
    for year in years:
        year_path = os.path.join(base_dir, str(year))
        create_directory(year_path)

# Get the current year
current_year = datetime.now().year

# Create a list of the past 5 years
years = [current_year - i for i in range(5)]

# Set the base directory to the current working directory
base_dir = os.getcwd()

# Create the directory structure
create_file_structure(base_dir, years)
