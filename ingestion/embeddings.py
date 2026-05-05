from sentence_transformers import SentenceTransformer


# Load model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list):
    """
    Convert chunks into embeddings
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings