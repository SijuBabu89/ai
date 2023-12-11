import pdfplumber
from datasets import Dataset


def extract_text_from_pdf(pdf_path):
    """
    A function to extract text from pdf file page by page.

    pdf_path: path to pdf file
    return: list of text from each page
    """
    with pdfplumber.open(pdf_path) as pdf:
        text_pages = [page.extract_text() for page in pdf.pages]
    return text_pages


def tokenize_text(example, tokenizer):
    """
    A function to tokenize text using tokenizer.

    example: text to tokenize
    tokenizer: tokenizer to use
    return: tokenized text
    """
    return tokenizer(example["text"], padding="max_length", truncation=True)


def prepare_dataset(text_pages):
    """
    A function to prepare dataset for fine-tuning.

    text_pages: list of text from each page
    return: dataset
    """
    dataset = Dataset.from_dict({"text": text_pages})
    return dataset


def tokenize_dataset(tokenize_fun, dataset):
    """
    A function to tokenize dataset by mapping it.

    tokenize_fun: function to tokenize dataset
    dataset: dataset to tokenize
    return: tokenized dataset
    """ 
    return dataset.map(tokenize_fun, batched=True)
