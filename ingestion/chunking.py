def chunk_text(pages: list, chunk_size=500, overlap=100):
    """
    Convert pages into overlapping chunks

    Returns:
    [
        {
            "text": "...",
            "page": 1
        }
    ]
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_num = page["page"]

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "page": page_num
            })

            start += chunk_size - overlap

    return chunks