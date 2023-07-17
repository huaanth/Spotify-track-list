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
    #going to use download the songs based on their id
    return ""
