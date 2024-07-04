from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO

def get_thumbnail(url, file_path="thumbnail.jpg", save=True):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    response = requests.get(thumbnail_url)
    img = Image.open(BytesIO(response.content))
    if save:
        img.save(file_path)

url = "https://youtu.be/XEETOp5jo9w?t=1163"
thumbnail = get_thumbnail(url)