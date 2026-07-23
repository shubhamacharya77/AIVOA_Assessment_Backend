import os

from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts raw text from a PDF file using LangChain's PyPDFLoader.
    Returns the concatenated text of all pages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Combine text from all pages
    full_text = "\n".join([page.page_content for page in pages])

    return full_text


def process_uploaded_file(file_path: str) -> str:
    """
    General utility to process uploaded complaint documents.
    Currently supports .pdf and .txt files.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(
            f"Unsupported file type: {ext}. Only PDF and TXT are supported."
        )
