from pypdf import PdfReader
import pathlib


file_path = pathlib.Path("../../data/01.2023Test.pdf")

print(file_path.is_file())

reader = PdfReader(file_path)
page = reader.pages[0]
print(page.extract_text())