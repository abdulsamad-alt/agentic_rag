import faiss
import pickle
import numpy as np


def build_faiss_index(embeddings, chunks):
    """
    Create FAISS index and store metadata
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index


def save_index(index, chunks, path="data/vector_db/"):
    """
    Save FAISS index + metadata
    """

    faiss.write_index(index, path + "index.faiss")

    with open(path + "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)


def load_index(path="data/vector_db/"):
    """
    Load FAISS index + metadata
    """

    index = faiss.read_index(path + "index.faiss")

    with open(path + "chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def search(index, query_embedding, chunks, top_k=5):
    """
    Search most relevant chunks
    """

    D, I = index.search(np.array([query_embedding]), top_k)

    results = [chunks[i] for i in I[0]]

    return results