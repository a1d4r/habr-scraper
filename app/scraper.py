import asyncio
import itertools
import logging
import sys
from pathlib import Path
from typing import List

import aiofiles
import typer
from aiohttp import ClientSession
from aiohttp.web import HTTPException

from app import settings
from app.parser import HabrArticleParser, HabrFeedParser
from app.utils import to_valid_filename

logger = logging.getLogger(__name__)
logger.disabled = not settings.DETAILED_LOGS


async def get_article_urls_from_page(session: ClientSession, page: int) -> List[str]:
    async with session.get(
        f'{settings.BASE_URL}/page{page}/', timeout=settings.RESPONSE_TIMEOUT
    ) as response:
        response.raise_for_status()
        feed_parser = HabrFeedParser(await response.text())
        return feed_parser.get_article_urls()


async def get_image_from_url(session: ClientSession, url: str) -> bytes:
    async with session.get(url, timeout=settings.RESPONSE_TIMEOUT) as response:
        response.raise_for_status()
        return await response.read()


async def get_article_from_url(session: ClientSession, url: str) -> str:
    async with session.get(url, timeout=settings.RESPONSE_TIMEOUT) as response:
        response.raise_for_status()
        return await response.text()


async def save_article(session: ClientSession, url: str, path: Path) -> None:
    logger.info('Downloading article %s', url)

    article = await get_article_from_url(session, url)
    article_parser = HabrArticleParser(article)
    title = to_valid_filename(article_parser.get_title())
    text = article_parser.get_text()

    article_path = path / title
    article_path.mkdir(parents=True, exist_ok=True)

    # save text
    async with aiofiles.open(article_path / 'article.txt', 'w') as f:
        await f.write(text)

    logger.info('Downloading images for article %s', url)

    # save images
    for image_url in article_parser.get_image_urls():
        image = await get_image_from_url(session, image_url)
        filename = image_url.split('/')[-1]
        async with aiofiles.open(article_path / filename, 'wb') as fi:
            await fi.write(image)

    logger.info('Finished downloading article %s', url)


async def fetch_urls(num_articles: int) -> List[str]:
    num_pages = num_articles // settings.ARTICLES_PER_PAGE + 1

    tasks = []
    async with ClientSession() as session:
        for page in range(1, num_pages + 1):
            tasks.append(get_article_urls_from_page(session, page))

        try:
            result = await asyncio.gather(*tasks)
        except HTTPException as e:
            typer.echo(f'Failed to fetch urls for articles: {e}', err=True)
            sys.exit(1)

    return list(itertools.chain(*result))[:num_articles]


async def download_articles(article_urls: List[str], path: Path) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in article_urls:
            tasks.append(save_article(session, url, path))

        try:
            await asyncio.gather(*tasks)
        except HTTPException as e:
            typer.echo(f'Failed to download article: {e}', err=True)


async def save_articles(num_articles: int, path: Path) -> None:
    typer.echo('Fetching urls for articles')
    article_urls = await fetch_urls(num_articles)
    typer.echo('Starting downloading articles...')
    await download_articles(article_urls, path)
    typer.echo('Finished downloading articles')
