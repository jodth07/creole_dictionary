import random
from typing import Optional


class ImageFetcher:

    def __init__(self):
        # Placeholder fallback images
        self.fallback_images = {
            "chen": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Dog_Breeds.jpg",
            "chat": "https://upload.wikimedia.org/wikipedia/commons/a/a3/81_INF_DIV_SSI.jpg",
            "manje": "https://upload.wikimedia.org/wikipedia/commons/6/69/Food_pyramide.jpg"
        }

    def get_image(self, word: str) -> Optional[str]:
        # Simulate real image fetching
        return self.fallback_images.get(word.lower()) or None
