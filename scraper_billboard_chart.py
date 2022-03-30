from scraper import Scraper
from bs4.element import Tag
from typing import List


PAGE_URL_PREFIX = "https://www.billboard.com/charts/hot-100"
SONG_TITLE_SELECTORS = ".o-chart-results-list__item #title-of-a-story"
ARTIST_SELECTORS = ".o-chart-results-list__item c-label"


class ScraperBillboardChart(Scraper):

    def __init__(self, date: str) -> None:
        self.set_page_url(date)
        super().__init__(self.page_url)
        

    def set_page_url(self, date: str) -> None:
        page_url = f"{PAGE_URL_PREFIX}/{date}/"
        self.page_url = page_url


    def get_all_songs(self, selector = SONG_TITLE_SELECTORS) -> List[dict]:
        self.chart_song_titles = []
        elements = self.soup.select(selector)
        for element in elements:
            song = ScraperBillboardChart.get_song_data(element)    
            self.chart_song_titles.append(song)


    @staticmethod
    def get_song_data(element: Tag) -> str:
        song_title = element.get_text().strip()
        artist_name = element.find_next_sibling().get_text().strip()
        song = {
            "song_title": song_title,
            "artist_name": artist_name
            }
        return song
