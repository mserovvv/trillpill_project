
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from slugify import slugify

ARTIST = "Thrill Pill"
ALBUMS = [
    "Chelsea",
    "Chelsea 2",
    "Fuelle Noir",
    "Откровения",
    "Московские Хроники",
    "Грустное",
    "Chelsea 3",
    "Искренне я",
    "BM24",
]
BASE_URL = "https://genius.com"
OUTPUT_FILE = Path("data/thrillpill_lyrics.jsonl")


def get_album_tracks(album: str) -> list[dict]:
    artist_slug = slugify(ARTIST)
    album_slug = slugify(album)
    url = f"{BASE_URL}/albums/{artist_slug}/{album_slug}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="album_track-name_link")
    return [
        {"title": link.text.strip(), "album": album, "url": link["href"]}
        for link in links
    ]


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for album in ALBUMS:
            for track in get_album_tracks(album):
                f.write(json.dumps(track, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
