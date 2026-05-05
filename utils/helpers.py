import re


def clean_text(text: str) -> str:
    """
    Basic cleaning:
    - remove extra spaces
    - remove weird characters
    - fix line breaks
    """

    # Remove multiple newlines
    text = re.sub(r"\n+", "\n", text)

    # Remove multiple spaces
    text = re.sub(r"[ ]+", " ", text)

    # Remove unwanted symbols (optional tweak)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()


def remove_repeated_lines(text: str) -> str:
    """
    Remove duplicate lines (common in PDFs headers/footers)
    """

    lines = text.split("\n")
    seen = set()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line and line not in seen:
            seen.add(line)
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def normalize_text(text: str) -> str:
    """
    Normalize text:
    - lowercase
    """

    return text.lower()


def preprocess_pages(pages: list) -> list:
    """
    Apply all preprocessing steps page-wise
    """

    processed = []

    for page in pages:
        text = page["text"]

        text = clean_text(text)
        text = remove_repeated_lines(text)
        text = normalize_text(text)

        processed.append({
            "page": page["page"],
            "text": text
        })

    return processed