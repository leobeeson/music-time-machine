# Musical Time Machine

## Behavior:
1. Application asks user for a date -> {DATE}.
2. Application gets the Billboard Top 100 list of songs for {DATE}.
3. Application creates a Spotify playlist with the Billboard Top 100 list of songs for {DATE}.
4. A new playlist appears in the user's Spotify page.

## Requirements:
1. Create a [Spotify account](https://www.spotify.com/uk/).
2. Create a new [Spotify App](https://developer.spotify.com/dashboard/login).
3. Copy your `Client ID` and `Client Secret` from your Spotify App.
4. Create a file called `.env`, add your Spotify App credentials to the following variables, and include a callback URL (the example below `https://example.com/callback/` works just fine):
    ```txt
    SPOTIPY_CLIENT_ID={Client ID}
    SPOTIPY_CLIENT_SECRET={Client Secret}
    SPOTIPY_REDIRECT_URI="https://example.com/callback/"
    ```
5. Run `main.py`.

## Variations:
- You can scrape different Billboard lists. 
- For example, for Latin songs, you can change the global variable `PAGE_URL_PREFIX` in scraper_billboard_chart.py to this:
```python
PAGE_URL_PREFIX = "https://www.billboard.com/charts/latin-songs/"
```

## Caution:
### Spotify Access Token and Credentials
- When instantiating the `SpotifyClient()` class (from spotify_client.py), the `authenticate` method called by the constructor (i.e. `__init__`) will create a `token.txt` containing your Spotify access token in the project's root folder. 
- Though the access token is only valid for 60 minutes, be careful with it.
- The `token.txt` file, with along the `.env` file containing your credentials, **is currently included in the `.gitignore` file**, but avoid removing them from it.

## Credits:
- This project was motivated by the course [100 Days of Code: The Complete Python Pro Bootcamp for 2022](https://www.udemy.com/course/100-days-of-code/learn/), the [Day 46 project](https://www.udemy.com/course/100-days-of-code/learn/lecture/21839862#questions).

