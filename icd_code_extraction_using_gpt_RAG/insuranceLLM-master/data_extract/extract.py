import os
import re

import PyPDF2
import json

def extract_to_txt(file_path, output_file_path):
    """This function is used to extract text from a PDF file

    :param file_path: The path to the PDF file
    :type file_path: str
    :return: str -- The extracted text from the PDF file
    :raises: None
    """
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
    with open(output_file_path, 'w') as file:
        for page in range(2, len(pdfReader.pages)):
            pageObj = pdfReader.pages[page]
            file.write(pageObj.extract_text())

    print("Text extracted successfully.")


def extract_icd(text):
    """This function is used to extract ICD codes and their descriptions from a text

    :param text: The text from which the ICD codes are to be extracted
    :type text: str
    :return: list -- The list of ICD codes and their descriptions
    :raises: None
    """

    lines=[]
    disease_codes = []
    disease_names = []

    for line in text.split('\n'):
        lines.append(line)

    for item in lines:
        match = re.match(r'[A-Z0-9]+\.[A-Z0-9]+',item)
        if match:
            code = match.group(0)
            name = item[match.end():].strip()
            disease_codes.append(code)
            disease_names.append(name)

    return disease_codes,disease_names