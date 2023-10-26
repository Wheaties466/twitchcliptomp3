import yt_dlp
import sys
import os
import re

OUTPUT_DIR = "output"

def is_valid_twitch_url(url):
    pattern = re.compile(r'^https://clips\.twitch\.tv/[A-Za-z0-9]+')
    return bool(pattern.match(url))

def get_unique_filename(filename):
    counter = 1
    new_filename = filename
    
    while os.path.exists(new_filename):
        name, extension = os.path.splitext(filename)
        new_filename = f"{name}_{counter}{extension}"
        counter += 1
    
    return new_filename

def download_clip(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': get_unique_filename('temp_video.mp4'), 
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return info_dict.get('title', None), ydl.prepare_filename(info_dict)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <twitch_clip_url>")
        sys.exit(1)
    
    url = sys.argv[1]

    if not is_valid_twitch_url(url):
        print("Invalid Twitch clip URL.")
        sys.exit(1)

    title, filename = download_clip(url)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    if title:
        output_filename = f"{OUTPUT_DIR}/{title}.mp4".replace(" ", "_")
        output_filename = get_unique_filename(output_filename)
        os.rename(filename, output_filename)
    else:
        output_filename = get_unique_filename(f"{OUTPUT_DIR}/{filename}")
        os.rename(filename, output_filename)

    print(f"Download completed. Check {output_filename} for the video!")
