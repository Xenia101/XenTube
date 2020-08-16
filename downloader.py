from typing import *
from pytube import YouTube
import os

def dircheck(outpath: str):
    return os.path.isdir(outpath)
        
def download(URL:str, outpath:str):
    if dircheck(outpath) is True:
        print("Download..")
        yt = YouTube(URL)
        yt.streams.first().download(output_path=outpath)
    else:
        print("Path failed..")
        return 0
