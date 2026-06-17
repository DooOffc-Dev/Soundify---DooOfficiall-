from fastapi import FastAPI
from ytmusicapi import YTMusic
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()
home_cache = {}
CACHE_TTL = 3600 # 1 Jam

def format_results(search_results):
    cleaned_results = []
    for item in search_results:
        if 'videoId' in item:
            cleaned_results.append({
                "videoId": item['videoId'],
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists', [{'name': 'Unknown Artist'}])[0]['name'] if 'artists' in item else 'Unknown Artist',
                "thumbnail": item['thumbnails'][-1]['url'] if 'thumbnails' in item else ''
            })
    return cleaned_results

@app.get("/api/search")
def search_music(query: str):
    try:
        search_results = ytmusic.search(query, filter="songs", limit=15)
        return {"status": "success", "data": format_results(search_results)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/home")
def get_home_data():
    current_time = time.time()
    if "data" in home_cache and (current_time - home_cache["timestamp"] < CACHE_TTL):
        return {"status": "success", "data": home_cache["data"]}

    try:
        data = {
            "recent": format_results(ytmusic.search('lagu hits indonesia 2025', filter="songs", limit=6)),
            "trending": format_results(ytmusic.search('trending music indonesia', filter="songs", limit=10)),
            "chill": format_results(ytmusic.search('lagu santai cafe indonesia', filter="songs", limit=10)),
            "galau": format_results(ytmusic.search('lagu galau indonesia terbaik', filter="songs", limit=10))
        }
        home_cache["data"] = data
        home_cache["timestamp"] = current_time
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
