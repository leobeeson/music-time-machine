from bs4 import BeautifulSoup
import requests
from typing import List


class Scraper:

    def __init__(self, page_url) -> None:
        self.page_url = page_url
        self.get_page()
        self.create_soup()
    

    def get_page(self):
        response = requests.get(self.page_url)
        content = response.text
        self.content = content

    
    def create_soup(self):
        soup = BeautifulSoup(self.content, "html.parser")
        self.soup = soup


    def get_elements_by_single_class(self, class_name: str) -> List[str]:
        elements = self.soup.find_all(class_=class_name)
        texts = []
        for element in elements:
            text = element.getText()
            texts.append(text)
        return texts
