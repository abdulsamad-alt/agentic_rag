import re
import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion.vector_store import load_index


class QueryRouter:
    def __init__(self):
        # embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # load FAISS
        self.index, self.chunks = load_index()

    # -------------------------
    # BASIC CHECKS
    # -------------------------

    def is_valid(self, query):
        return len(query.strip()) > 2

    def is_greeting(self, query):
        q = query.lower().strip()

        patterns = [
            r"^hi$",
            r"^hello$",
            r"^hey$",
            r"^hii$",
            r"^how are you$",
            r"^how r u$",
            r"^what's up$",
            r"^wassup$"
        ]

        return any(re.match(p, q) for p in patterns)

    def is_casual(self, query):
        q = query.lower().strip()

        patterns = [
            r"^who are you$",
            r"^what can you do$",
            r"^tell me a joke$",
            r"^your name$"
        ]

        return any(re.match(p, q) for p in patterns)

    def is_gibberish(self, query):
        words = query.split()
        if len(words) == 0:
            return True

        avg_len = sum(len(w) for w in words) / len(words)
        return avg_len > 12

    # -------------------------
    # RELEVANCE CHECK
    # -------------------------

    def is_relevant_to_doc(self, query):
        query_vec = self.model.encode(query)

        D, I = self.index.search(np.array([query_vec]), 1)
        score = D[0][0]

        return score < 1.2, score

    # -------------------------
    # COMPLEXITY
    # -------------------------

    def is_complex(self, query):
        return len(query.split()) > 12 or "and" in query.lower()

    # -------------------------
    # MAIN ROUTER
    # -------------------------

    def route(self, query):
        query = query.strip()

        if not self.is_valid(query):
            return {"route": "invalid"}

        if self.is_greeting(query):
            return {"route": "greeting"}

        if self.is_casual(query):
            return {"route": "casual"}

        if self.is_gibberish(query):
            return {"route": "gibberish"}

        is_relevant, score = self.is_relevant_to_doc(query)
        is_complex = self.is_complex(query)

        if is_relevant and not is_complex:
            return {"route": "retrieval"}

        return {"route": "llm"}