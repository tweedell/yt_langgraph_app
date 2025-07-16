from youtube_search import YoutubeSearch
import yt_dlp

# Step 1: Define the search term and number of videos
SEARCH_TERM = "Ukrainian drone footage"
MAX_RESULTS = 2  # You can increase this

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
for i, video in enumerate(videos_search):
    title = video['title']
    url_suffix = video['url_suffix']
    print(f"\n[{i+1}] Downloading: {title}")
    try:
        #ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download(['https://www.youtube.com' + url_suffix])
    except Exception as e: # Catching a general exception and storing it in 'e'
        print(f"An error occurred: {e}")
    else:
        print(f"Number successfully processed.")
    finally:
        print(f"Program execution complete.")


