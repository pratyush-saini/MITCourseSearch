from youtube_transcript_api import YouTubeTranscriptApi 
import pandas as pd
from multiprocessing import Pool
from pytube import YouTube
# import requests
# from PIL import Image
# from io import BytesIO
import time

def get_thumbnail(url, file_path="thumbnail.jpg", save=False):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    title = yt.title
    return thumbnail_url, title
    # response = requests.get(thumbnail_url)
    # img = Image.open(BytesIO(response.content))
    # if save:
    #     img.save(file_path)
        
length_in_seconds = 100
output_file = "mit_ocw.csv"
youtube_links_file = "mitocw-202407031516.list"
# youtube_links_file = "small_list.txt"
youtube_links = []
with open(youtube_links_file, "r") as file:
    for line in file:
        youtube_links.append(line.strip())
        
def convert_seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"

def create_permalink(video_id, timestamp):
    return f"https://youtu.be/{video_id}&t={int(timestamp)}"

class Chunk:
    def __init__(self, title, text, perma_link, thumbnail_link):
        self.title=title
        self.text = text
        self.perma_link = perma_link
        self.thumbnail_link = thumbnail_link
        
import tqdm

def process_link(link):
    data = []
    y_id = link.split("?v=")[1]
    try:
        srt = YouTubeTranscriptApi.get_transcript(y_id, languages=['en'])
        time.sleep(2)
    except:
        return []
    text_chunks = [""]
    timestamps = [srt[0]['start']]
    current_duration = 0
    for item in srt:
        current_duration += item['duration']
        if current_duration > length_in_seconds:
            current_duration = item['duration']
            text_chunks.append(item['text'])
            timestamps.append(float(item['start']))
        else:
            text_chunks[-1] = text_chunks[-1] + " " + item['text']
    for text, timestamp in zip(text_chunks, timestamps):
        perm_link = create_permalink(y_id, timestamp)
        thumbnail_link, title = get_thumbnail(perm_link)
        data.append(Chunk(title=title, text=text, perma_link=perm_link, thumbnail_link=thumbnail_link))
    return data

# for link in tqdm.tqdm(youtube_links):

import os

data = []

with Pool(processes=1) as pool:
    results = list(tqdm.tqdm(pool.imap(process_link, youtube_links), total=len(youtube_links)))
    data.extend(results)

# data = [process_link(link) for link in youtube_links]
df = pd.DataFrame(columns=['Id','Title','video_url','thumbnail','text'])

c = 0
for nested_list in data:
    for d in nested_list :
        df.loc[len(df)] = {"Id": c, "Title": d.title, "text": d.text.strip().replace("\n", " "), "video_url": d.perma_link, "thumbnail": d.thumbnail_link}
        c+=1
    
df.to_csv(output_file, index=False)


