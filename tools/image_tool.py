import google.generativeai as genai
from core.config import GEMINI_API_KEY
import os


class ImageTool:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

        self.image_dir = "data/images"

    def find_relevant_image(self, query):
        """
        VERY simple matching:
        (later we can improve)
        """
        files = os.listdir(self.image_dir)

        if not files:
            return None

        return os.path.join(self.image_dir, files[0])  # temp: first image

    def run(self, query):
        print("🖼 Using Image Tool...")

        image_path = self.find_relevant_image(query)

        if not image_path:
            return "No images available."

        with open(image_path, "rb") as f:
            image_data = f.read()

        response = self.model.generate_content([
            query,
            {"mime_type": "image/jpeg", "data": image_data}
        ])

        return response.text