from youtube_search import YoutubeSearch
import yt_dlp
import csv
import srt
import os
from datetime import timedelta
from pathlib import Path

# Step 1: Define the search term and number of videos
SEARCH_TERM = "Ukraine drone POV"
MAX_RESULTS = 1  # You can increase this
CSV_FILE = "/home/andrew/Tweedell/Sandtable/YT_LangGraph_App/yt_langgraph_app/Videos/yt_dl_metadata.csv"
SUBTITLE_LANG = "en"  # You can change to 'uk', 'ru', or 'all'
SUBTITLE_FORMAT = "srt"  # 'srt' or 'vtt'
QA_TRANSCRIPTS_DIR = "/home/andrew/Tweedell/Sandtable/YT_LangGraph_App/yt_langgraph_app/qa_transcripts"
VIDEO_DIR = "/home/andrew/Tweedell/Sandtable/YT_LangGraph_App/yt_langgraph_app/Videos"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(QA_TRANSCRIPTS_DIR, exist_ok=True)

# Step 2: Search YouTube
print(f"Searching YouTube for: {SEARCH_TERM}")
videos_search = YoutubeSearch(SEARCH_TERM, max_results=MAX_RESULTS).to_dict()

# Step 3: Define all relevant options and initialize downloader
ydl_opts = {
            'verbose': False,
            'format': 'best',
            'outtmpl': "%(id)s.%(ext)s",
            'paths': {'home': VIDEO_DIR},
            'writesubtitles': True,
            'subtitlesformat': SUBTITLE_FORMAT,        # Specify the desired format (e.g., 'srt', 'vtt')
            'subtitleslangs': [SUBTITLE_LANG],        # Specify the language(s) (e.g., 'en' for English)
            'writeautomaticsub': True       # Download automatically generated subtitles
            }

ydl = yt_dlp.YoutubeDL(ydl_opts)

metadata_fields = ['id',
                   'title',
                   'channel',
                   'duration',
                   'views',
                   'published',
                   'url',
                   'has_subs',
                   'word_count',
                   'long_desc',
                   'tags',
                   'dl_status']

with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
    
    writer = csv.DictWriter(csvfile, fieldnames=metadata_fields)
    writer.writeheader()

    # Step 4: Download each video using yt-dlp

    for i, video in enumerate(videos_search):
        
        title = video['title']
        url = 'https://www.youtube.com' + video['url_suffix']
        id = video['id']
        channel = video['channel']
        duration = video['duration']
        views = video['views']
        published = video['publish_time']
        long_desc = "N/A"
        tags = "N/A"
        has_subs = False

        try:
            info = ydl.extract_info(url, download=False)
            long_desc = info.get('description', '').strip().replace('\n', ' ')[:500]
            tags = ", ".join(info.get('tags', []))
            has_subs = True if 'subtitles' in info and info['subtitles'] else False
        except Exception as e:
            print(f"Failed to extract metadata: {e}")

        print(f"\n[{i+1}] Downloading: {title}")
        
        try:
            ydl.download([url])
            dl_status = "Success"
        except Exception as e: # Catching a general exception and storing it in 'e'
            print(f"An error occurred: {e}")
            dl_status = "Failed"
        else:
            print(f"Number successfully processed.")
        finally:
            print(f"Program execution complete.")

        # Step 5: Extract and format subtitle content
        srt_file = os.path.join(VIDEO_DIR, f"{id}.{SUBTITLE_LANG}.{SUBTITLE_FORMAT}")
        
        if os.path.exists(srt_file):
            
            try:
                
                with open(srt_file, 'r', encoding='utf-8') as f:
                    subs = list(srt.parse(f.read()))

                # Extract raw transcript
                full_text = " ".join([s.content for s in subs])
                transcript_path = os.path.join(QA_TRANSCRIPTS_DIR, f"{id}_transcript.txt")
                
                with open(transcript_path, 'w', encoding='utf-8') as out:
                    out.write(full_text)

                # Step 6: Format for QA (timestamped chunks)
                qa_chunks = []
                chunk = []
                chunk_word_limit = 80
                word_count = 0
                
                for s in subs:
                    words = s.content.split()
                    
                    if word_count + len(words) > chunk_word_limit:
                        start = chunk[0].start
                        end = chunk[-1].end
                        text = " ".join([x.content for x in chunk])
                        qa_chunks.append((start, end, text))
                        chunk = []
                        word_count = 0
                    chunk.append(s)
                    word_count += len(words)

                # Save QA-ready version
                qa_file = os.path.join(QA_TRANSCRIPTS_DIR, f"{id}_qa_chunks.txt")
                
                with open(qa_file, 'w', encoding='utf-8') as qaf:
                    
                    for start, end, text in qa_chunks:
                        qaf.write(f"[{start} - {end}]\n{text}\n\n")

                print(f"Transcript and QA-ready version saved for: {title}")

            except Exception as e:
                print(f"Subtitle parse error for {title}: {e}")

        # Write metadata to CSV
        writer.writerow({'id':id,
                        'title': title,
                        'channel': channel,
                        'duration': duration,
                        'views': views,
                        'published': published,
                        'dl_status': dl_status,
                        'tags': tags,
                        'has_subs': has_subs,
                        'word_count': word_count,
                        'long_desc':long_desc,
                        'url': url
                        })

print(f"\nMetadata saved to: {CSV_FILE}")
