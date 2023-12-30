import re
import os
from pathlib import Path
from PIL import Image
import pytesseract

file_path = Path("../../data/papa_ausgaben/ausgaben_0.jpg")

image = Image.open(file_path)
extracted_text = pytesseract.image_to_string(image)
print(extracted_text)