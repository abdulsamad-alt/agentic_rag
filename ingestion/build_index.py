from ingestion.loader import load_pdf
from utils.helpers import preprocess_pages
from ingestion.chunking import chunk_text
from ingestion.embeddings import create_embeddings
from ingestion.vector_store import build_faiss_index, save_index

import os


def main():
    # -------------------------
    # PATH FIX (IMPORTANT)
    # -------------------------
    pdf_path = "data/raw/sample.pdf"   # ✅ keep PDF inside repo

    if not os.path.exists(pdf_path):
        print("❌ PDF not found at:", pdf_path)
        return

    print("📄 Loading PDF...")
    pages = load_pdf(pdf_path)

    print("🧹 Preprocessing...")
    clean_pages = preprocess_pages(pages)

    print("✂️ Chunking...")
    chunks = chunk_text(clean_pages)

    print(f"🔢 Total chunks: {len(chunks)}")

    print("🧠 Creating embeddings (this may take time)...")
    embeddings = create_embeddings(chunks)

    print("📦 Building FAISS index...")
    index = build_faiss_index(embeddings, chunks)

    print("💾 Saving index...")
    save_index(index, chunks)

    print("✅ Done! Index saved.")


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    main()