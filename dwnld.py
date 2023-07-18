from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import requests
import youtube_dl
import pandas
import os

def ScrapeID(query):
    print("Getting video: ", query)
    basic = "http://www.youtube.com/results?search_query=" #it will just put the song name after the equal sign and find it on youtube
    url = (basic + query)
    url.replace(" ","+")
    page = requests.get(url)
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html,"html.parser")

    results = soup.find("a", id = "video-title")
    return results["href"].split('/watch?v=')[1]

def DownloadID(id):
    saved_path = str(os.path.join(Path.home,"Downloads/songs"))
    try:
        os.mkdir(saved_path)
    except:
        print("folder already exists")
    
    options = {
        "format": "bestaudio/best:",
        "postprocessors": [{'key': 'FFmpegExtractAudio',
        		'preferredcodec': 'mp3',
        		'preferredquality': '192',}],
        'outtmpl': saved_path + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(id)

def Downloadtitle(title):
    song_ids =[]
    for i, query in enumerate(title):
        vid_id = ScrapeID(query)
        song_ids += [vid_id]
    print("Downloading")
    DownloadID(song_ids)

def __main__():
    
    data = pandas.read_csv('songs.csv')
    data = data['column'].tolist()
    print("Downloading ", len(data), " songs")
    Downloadtitle(data[0:1])
__main__()
