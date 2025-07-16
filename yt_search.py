from youtube_search import YoutubeSearch
import yt_dlp
import csv

# Step 1: Define the search term and number of videos
SEARCH_TERM = "Ukrainian drone footage"
MAX_RESULTS = 2  # You can increase this
CSV_FILE = "/home/andrew/Tweedell/Sandtable/YT_LangGraph_App/yt_langgraph_app/Videos/yt_dl_metadata.csv"

# Step 2: Search YouTube
print(f"Searching YouTube for: {SEARCH_TERM}")
videos_search = YoutubeSearch(SEARCH_TERM, max_results=MAX_RESULTS).to_dict()

# Step 3: Define all relevant options and initialize downloader
ydl_opts = {
            'verbose': False,
            'format': 'best',
            'outtmpl': '%(title)s-%(id)s.%(ext)s',
            'paths': {'home': '/home/andrew/Tweedell/Sandtable/YT_LangGraph_App/yt_langgraph_app/Videos'},
            'writesubs': True,
            'subtitlesformat': 'srt',        # Specify the desired format (e.g., 'srt', 'vtt')
            'subtitleslangs': ['en'],        # Specify the language(s) (e.g., 'en' for English)
            'writeautomaticsubs': True       # Download automatically generated subtitles
            }

ydl = yt_dlp.YoutubeDL(ydl_opts)

# Step 4: Download each video using yt-dlp

metadata_fields = ['id', 'title', 'channel', 'duration', 'views', 'published', 'url', 'long_desc']

with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
    
    writer = csv.DictWriter(csvfile, fieldnames=metadata_fields)
    writer.writeheader()

    for i, video in enumerate(videos_search):
        
        title = video['title']
        url = 'https://www.youtube.com' + video['url_suffix']
        id = video['id']
        channel = video['channel']
        duration = video['duration']
        views = video['views']
        published = video['publish_time']
        long_desc = video['long_desc']

        print(f"\n[{i+1}] Downloading: {title}")
        
        try:
            ydl.download([url])
        except Exception as e: # Catching a general exception and storing it in 'e'
            print(f"An error occurred: {e}")
        else:
            print(f"Number successfully processed.")
        finally:
            print(f"Program execution complete.")

        # Write metadata to CSV
        writer.writerow({'id':id,
                        'title': title,
                        'channel': channel,
                        'duration': duration,
                        'views': views,
                        'published': published,
                        'long_desc':long_desc,
                        'url': url
                        })

print(f"\nMetadata saved to: {CSV_FILE}")
