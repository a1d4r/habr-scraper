from pathlib import Path

import pytest
from aiohttp import ClientSession

from app import scraper
from app.utils import to_valid_filename


@pytest.mark.usefixtures('mock_habr')
@pytest.mark.asyncio
async def test_get_article_links():
    articles = await scraper.fetch_urls(50)
    assert len(articles) == 50


@pytest.mark.usefixtures('mock_habr')
@pytest.mark.asyncio
async def test_get_image_from_url(client_session: ClientSession, image: bytes):
    assert (
        await scraper.get_image_from_url(
            client_session,
            'https://habrastorage.org/getpro/habr/post_images'
            '/4aa/da1/6fc/4aada16fc7ec94834a6c951ce5dc9cad.jpg',
        )
        == image
    )


@pytest.mark.usefixtures('mock_habr')
@pytest.mark.asyncio
async def test_get_article_from_url(client_session: ClientSession, article_html: str):
    assert (
        await scraper.get_article_from_url(
            client_session, 'https://habr.com/ru/post/551328/'
        )
        == article_html
    )


@pytest.mark.usefixtures('mock_habr')
@pytest.mark.asyncio
async def test_save_article(client_session: ClientSession, tmp_path: Path):
    await scraper.save_article(
        client_session, 'https://habr.com/ru/post/551328/', tmp_path
    )
    dirname = to_valid_filename('Digital-мероприятия в Москве c 19 по 25 июля')

    assert (tmp_path / dirname).exists()
    assert (tmp_path / dirname / 'article.txt').exists()


@pytest.mark.usefixtures()
@pytest.mark.asyncio
async def test_save_articles(tmp_path: Path):
    await scraper.save_articles(1, tmp_path)
    dirname = to_valid_filename('Digital-мероприятия в Москве c 19 по 25 июля')

    assert (tmp_path / dirname).exists()
    assert (tmp_path / dirname / 'article.txt').exists()
