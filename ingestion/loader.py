import fitz  


def load_pdf(file_path: str):
    """
    Load PDF and extract text page by page.

    Returns:
        List of dicts:
        [
            {"page": 1, "text": "..."},
            {"page": 2, "text": "..."}
        ]
    """

    document = fitz.open(file_path)

    pages = []

    for page_num in range(len(document)):
        page = document[page_num]

        text = page.get_text("text")

        text = text.strip()

        if text:  # skip empty pages
            pages.append({
                "page": page_num + 1,
                "text": text
            })

    document.close()

    return pages