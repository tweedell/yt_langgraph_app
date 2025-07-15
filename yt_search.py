from youtubesearchpython import VideosSearch
import subprocess
import os

# Step 1: Define the search term and number of videos
SEARCH_TERM = "Ukrainian drone footage"
MAX_RESULTS = 5  # You can increase this

# Step 2: Search YouTube
print(f"Searching YouTube for: {SEARCH_TERM}")
videos_search = VideosSearch(SEARCH_TERM, limit=MAX_RESULTS)
results = videos_search.result()['result']

# Step 3: Download each video using yt-dlp
for i, video in enumerate(results):
    title = video['title']
    url = video['link']
    print(f"\n[{i+1}] Downloading: {title}")
    try:
        subprocess.run([
            'yt-dlp',
            '-f', 'bestvideo+bestaudio/best',
            '-o', f"{title}.%(ext)s",
            url
        ], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to download: {title}")
