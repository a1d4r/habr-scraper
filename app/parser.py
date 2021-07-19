from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app import settings


class HabrFeedParser:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_article_urls(self) -> List[str]:
        return [
            urljoin(settings.BASE_URL, match['href'])
            for match in self.soup.find_all(class_='tm-article-snippet__title-link')
        ]


class HabrArticleParser:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_text(self) -> str:
        return self.soup.find(id='post-content-body').text

    def get_title(self) -> str:
        return self.soup.find(class_='tm-article-snippet__title').text

    def get_image_urls(self) -> List[str]:
        return [
            urljoin(settings.BASE_URL, match['src'])
            for match in self.soup.find(id='post-content-body').find_all('img')
        ]
