from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():
    headers = {
        "Authorization": "api_key.client_access_token",
    }

    params = (("per_page", "50"),)

    response = requests.get(
        "https://api.genius.com/artists/1177/songs", headers=headers, params=params
    )

    if response.status_code == 200:
        songs = response.json()["response"]["songs"]
        lyrics = []

        for song in songs:
            url = song["url"]
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            lyrics_tag = soup.find("div", class_="lyrics")
            if lyrics_tag:
                lyrics_text = lyrics_tag.get_text().strip()
                lyrics.append(lyrics_text)

        return render_template("index.html", lyrics=lyrics)
    else:
        return "Error retrieving songs from Genius API"


if __name__ == "__main__":
    app.run(debug=True)
