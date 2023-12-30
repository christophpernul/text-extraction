import re
import os
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path

# Dictionary mapping month names to numbers
MONTHS = {
    "Januar": "01", # keine Umlaute in Zeitnachweisen
    "Jänner": "01",
    "Februar": "02",
    "März": "03",
    "Marz": "03", # keine Umlaute in Zeitnachweisen
    "April": "04",
    "Mai": "05",
    "Juni": "06",
    "Juli": "07",
    "August": "08",
    "September": "09",
    "Oktober": "10",
    "November": "11",
    "Dezember": "12"
}
# Regex expression to find "MONTH - YEAR" in text
REGEX_OLD_ZEITNACHWEIS = r"\b(?:Januar|Janner|Jänner|Februar|März|Marz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember) - \d{4}\b"
REGEX_NEW_ZEITNACHWEIS = r"\b\d{2}\.\d{2}\.\d{4}\b"

# Folder Path to your PDF files
directory = Path('../../data')

def extract_text_from_image_pdf(pdf_path):
    # Convert PDF to list of images
    images = convert_from_path(pdf_path)

    # OCR each image and collect text
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)

    return text


def extract_year_month_new_version(text: str, regex: str) -> str:
    """Extracts pattern "dd.mm.yyyy" from a string of the new Zeitnachweis."""
    match = re.search(regex, text)
    if match:
        match = match.group()
        year_month = match.split(".")[2] + "-" + match.split(".")[1]
    else:
        year_month = None
    return year_month

def extract_year_month_old_version(text: str, regex: str) -> str:
    """Extracts pattern "MONTH - YEAR" from a string of the old Zeitnachweis."""
    match = re.search(regex, text)
    if match:
        year_month = match.group()
        year_month = convert_year_month(year_month)
    else:
        year_month = None
    return year_month

def convert_year_month(text: str) -> str:
    month_name = text.split("-")[0].strip()
    year = text.split("-")[1].strip()
    month_number = MONTHS[month_name]
    return f"{year}-{month_number}"


for filepath in directory.iterdir():
    if filepath.suffix == '.pdf':  # Check for specific file extensions
        print(f"Extracting file in {filepath}.")
        extracted_text = extract_text_from_image_pdf(filepath)

        # IMPORTANT: Change the following line whether a NEW or OLD version of the Zeitnachweis should be parsed!
        # year_month = extract_year_month_old_version(extracted_text, regex=REGEX_OLD_ZEITNACHWEIS)
        year_month = extract_year_month_new_version(extracted_text, regex=REGEX_NEW_ZEITNACHWEIS)

        if year_month is not None:
            print(f"\tFound the date: {year_month}")
            filename_new = f"{year_month}.pdf"
            filepath_renamed = filepath.parent.joinpath(filename_new)
            os.rename(filepath, filepath_renamed)
            print(f"\tRenamed file '{filepath}' to '{filepath_renamed}'!")
        else:
            print(f"\tNo date found in file: {filepath}")

print("Finished!")
