from typing import List

from bs4 import BeautifulSoup


class HabrFeedParser:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_article_urls(self) -> List[str]:
        return [
            match['href'] for match in self.soup.find_all(class_='post__title_link')
        ]


class HabrArticleParser:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_text(self) -> str:
        return self.soup.find(class_='post__body_full').text

    def get_title(self) -> str:
        return self.soup.title.text

    def get_image_urls(self) -> List[str]:
        return [
            match['src']
            for match in self.soup.find(class_='post__body_full').find_all('img')
        ]
