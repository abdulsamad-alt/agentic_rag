from ingestion.loader import load_pdf
from utils.helpers import preprocess_pages
from ingestion.chunking import chunk_text
from ingestion.embeddings import create_embeddings
from ingestion.vector_store import build_faiss_index, save_index

pdf_path = "2515-9th Class Computer Science New SNC Punjab Textbook PDF-by-Admin-(taleem360.com).pdf"

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



# from ingestion.image_extractor import extract_images

# extract_images("2515-9th Class Computer Science New SNC Punjab Textbook PDF-by-Admin-(taleem360.com).pdf")
# print("✅ Images extracted")