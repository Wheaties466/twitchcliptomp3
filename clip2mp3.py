import yt_dlp as youtube_dl
from moviepy.editor import *
import sys
import os
import re

def is_valid_twitch_url(url):
    # Check if it's a Twitch clip URL format (this can change based on Twitch's URL scheme)
    pattern = re.compile(r'^https://clips\.twitch\.tv/[A-Za-z0-9]+')
    return bool(pattern.match(url))

def is_video_file(filename):
    # Check file magic bytes for common video formats
    video_magic_bytes = [
        b'\x00\x00\x00 ftypisom',  # MP4
        b'\x1aE\xdf\xa3'           # MKV (WebM also has this signature but different segments)
    ]
    with open(filename, 'rb') as file:
        file_start = file.read(16)
        for magic in video_magic_bytes:
            if file_start.startswith(magic):
                return True
    return False

def download_clip(url, filename="clip.mp4"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]',  # download the best mp4 format available
        'outtmpl': filename,             # name of the file
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_to_mp3(video_filename, audio_filename="output.mp3"):
    clip = AudioFileClip(video_filename)
    clip.write_audiofile(audio_filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <twitch_clip_url>")
        sys.exit(1)

    url = sys.argv[1]

    if not is_valid_twitch_url(url):
        print("Invalid Twitch clip URL.")
        sys.exit(1)

    download_clip(url)

    if not is_video_file("clip.mp4"):
        print("Downloaded file is not a valid video format.")
        os.remove("clip.mp4")
        sys.exit(1)

    convert_to_mp3("clip.mp4")
    print("Conversion done. Check output.mp3 for the audio!")
