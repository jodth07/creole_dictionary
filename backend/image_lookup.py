import random
from typing import Optional


class ImageFetcher:
    def __init__(self):
        self.fallback_images = {
            "manje": "https://loveforhaitianfood.com/wp-content/uploads/2020/10/Website-Diri-Djondjon.jpg",
            "chen": "https://images6.fanpop.com/image/photos/40900000/Puppy-dogs-40949099-1280-1115.jpg",
            "chat": "https://wallpaperaccess.com/full/10046610.jpg"
        }

    def get_image(self, word: str) -> Optional[str]:
        return self.fallback_images.get(word.lower())
