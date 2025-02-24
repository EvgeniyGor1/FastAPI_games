from PIL import Image
import os


async def create_img_file(path: str):
    img = Image.new("RGB", (32, 64), color="white")
    img.save(path)


async def delete_img_file(path: str):
    os.remove(path)
