from ingestion.vector_store import load_index, search
from sentence_transformers import SentenceTransformer


class RetrieverTool:
    def __init__(self):
        print("📦 Loading vector database...")

        self.index, self.chunks = load_index()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("✅ Retriever ready")

    def run(self, query: str, top_k=5):
        """
        Retrieve relevant chunks for a query
        """

        print("🔍 Retrieving relevant context...")

        query_embedding = self.model.encode(query)

        results = search(self.index, query_embedding, self.chunks, top_k)

        # Combine results into one context
        context = "\n\n".join(
            [f"(Page {r['page']}) {r['text']}" for r in results]
        )

        return context