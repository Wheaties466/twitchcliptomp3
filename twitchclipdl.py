import yt_dlp as youtube_dl
import sys
import os
import re

TEMP_VIDEO_FILENAME = "temp_video.mp4"

def is_valid_twitch_url(url):
    pattern = re.compile(r'^https://clips\.twitch\.tv/[A-Za-z0-9]+')
    return bool(pattern.match(url))

def download_clip(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': TEMP_VIDEO_FILENAME,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        return title  # Return the video title

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
    
    output_filename = f"{title}.mp4".replace(" ", "_")  # Replacing spaces with underscores for filename
    
    os.rename(TEMP_VIDEO_FILENAME, output_filename)  # Renaming the temporary file to the title of the clip

    print(f"Download complete. Check {output_filename} for the video!")
