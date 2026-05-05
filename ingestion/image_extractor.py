import fitz  # PyMuPDF
import os


def extract_images(pdf_path, output_dir="data/images"):
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    image_paths = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            ext = base_image["ext"]

            filename = f"page{page_num+1}_img{img_index}.{ext}"
            path = os.path.join(output_dir, filename)

            with open(path, "wb") as f:
                f.write(image_bytes)

            image_paths.append({
                "page": page_num + 1,
                "path": path
            })

    return image_paths