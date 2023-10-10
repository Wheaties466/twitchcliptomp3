import yt_dlp as youtube_dl
from moviepy.editor import *
import sys
import os
import yt_dlp
import re
from pydub import AudioSegment

TEMP_VIDEO_FILENAME = "temp_video.mp4"

def is_valid_twitch_url(url):
    pattern = re.compile(r'^https://clips\.twitch\.tv/[A-Za-z0-9]+')
    return bool(pattern.match(url))

def is_video_file(filename):
    video_magic_bytes = [
        b'\x00\x00\x00 ftypisom',  # MP4
        b'\x1aE\xdf\xa3'           # MKV
    ]
    with open(filename, 'rb') as file:
        file_start = file.read(16)
        for magic in video_magic_bytes:
            if file_start.startswith(magic):
                return True
    return False

def download_clip(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': TEMP_VIDEO_FILENAME,
        'postprocessors': [],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        return title  # Return the video title

def convert_to_mp3(video_filename, audio_filename):
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

    title = download_clip(url)

    if not title:
        print("Couldn't fetch the title for the clip.")
        sys.exit(1)
    
    output_filename = f"{title}.mp3".replace(" ", "_")  # Replacing spaces with underscores for filename
    
    if not is_video_file(TEMP_VIDEO_FILENAME):
        print("Downloaded file is not a valid video format.")
        os.remove(TEMP_VIDEO_FILENAME)
        sys.exit(1)

    convert_to_mp3(TEMP_VIDEO_FILENAME, output_filename)
    print(f"Conversion done. Check {output_filename} for the audio!")
