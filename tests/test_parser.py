from typing import List

from app.parser import HabrArticleParser, HabrFeedParser


def test_get_article_links_from_html(habr_html: str, article_urls: List[str]):
    feed_parser = HabrFeedParser(habr_html)
    assert feed_parser.get_article_urls() == article_urls


def test_get_article_text(article_html: str, article_text_fragments: List[str]):
    article_parser = HabrArticleParser(article_html)
    text = article_parser.get_text()
    for fragment in article_text_fragments:
        assert fragment in text


def test_get_article_title(article_html: str):
    article_parser = HabrArticleParser(article_html)
    expected = 'Digital-мероприятия в Москве c 19 по 25 июля'
    assert article_parser.get_title() == expected


def test_get_image_urls_from_article_html(article_html: str, image_urls: List[str]):
    article_parser = HabrArticleParser(article_html)
    assert article_parser.get_image_urls() == image_urls
