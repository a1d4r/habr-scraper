from pathlib import Path

import pytest

from app import scraper
from app.utils import to_valid_filename


@pytest.mark.usefixtures('mock_habr')
def test_get_article_links():
    articles = scraper.fetch_urls(4, 50)
    assert len(articles) == 50


@pytest.mark.usefixtures('mock_habr')
def test_get_image_from_url(image: bytes):
    assert (
        scraper.get_image_from_url(
            'https://habrastorage.org/getpro/habr/post_images'
            '/4aa/da1/6fc/4aada16fc7ec94834a6c951ce5dc9cad.jpg'
        )
        == image
    )


@pytest.mark.usefixtures('mock_habr')
def test_get_article_from_url(article_html: str):
    assert (
        scraper.get_article_from_url('https://habr.com/ru/post/551328/') == article_html
    )


@pytest.mark.usefixtures('mock_habr')
def test_save_article(tmp_path: Path):
    scraper.save_article('https://habr.com/ru/post/551328/', tmp_path)
    dirname = to_valid_filename('Кто помнит «старшего брата» CD и DVD? / Хабр')

    assert (tmp_path / dirname).exists()
    assert (tmp_path / dirname / 'article.txt').exists()


@pytest.mark.usefixtures('mock_habr')
def test_save_articles(tmp_path: Path):
    scraper.save_articles(1, 1, tmp_path)
    dirname = to_valid_filename('Кто помнит «старшего брата» CD и DVD? / Хабр')

    assert (tmp_path / dirname).exists()
    assert (tmp_path / dirname / 'article.txt').exists()
