from scraper_billboard_chart import ScraperBillboardChart
from spotify_client import SpotifyClient

PLAYLIST_SUFFIX = "Billboard 100"

def create_time_machine_playlist():
    date = input("To which date do you want to travel to? Type the date in this format YYYY-MM-DD:")
    scraper = ScraperBillboardChart(date)   
    scraper.get_all_songs()
    spotify_client = SpotifyClient()
    song_ids = spotify_client.get_all_spotify_song_ids(scraper.chart_song_titles)
    song_uris = spotify_client.get_spotify_song_uris(song_ids)
    playlist_name = f"{date} {PLAYLIST_SUFFIX}"
    spotify_client.create_spotify_playlist(song_uris, playlist_name)

if __name__ == "__main__":
    create_time_machine_playlist()
