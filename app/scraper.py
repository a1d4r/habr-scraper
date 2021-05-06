import concurrent.futures
import logging
from pathlib import Path
from typing import List

import requests
import typer
from requests import RequestException

from app import settings
from app.parser import HabrArticleParser, HabrFeedParser
from app.utils import to_valid_filename

logger = logging.getLogger(__name__)
logger.disabled = not settings.DETAILED_LOGS


def get_article_urls_from_page(page: int) -> List[str]:
    response = requests.get(
        f'{settings.BASE_URL}/page{page}/', timeout=settings.RESPONSE_TIMEOUT
    )
    response.raise_for_status()
    feed_parser = HabrFeedParser(response.text)
    return feed_parser.get_article_urls()


def get_image_from_url(url: str) -> bytes:
    response = requests.get(url, timeout=settings.RESPONSE_TIMEOUT)
    response.raise_for_status()
    return response.content


def get_article_from_url(url: str) -> str:
    response = requests.get(url, timeout=settings.RESPONSE_TIMEOUT)
    response.raise_for_status()
    return response.text


def save_article(url: str, path: Path) -> None:
    logger.info('Downloading article %s', url)

    article = get_article_from_url(url)
    article_parser = HabrArticleParser(article)
    title = to_valid_filename(article_parser.get_title())
    text = article_parser.get_text()

    article_path = path / title
    article_path.mkdir(parents=True, exist_ok=True)

    # save text
    with (article_path / 'article.txt').open('w') as f:
        f.write(text)

    logger.info('Downloading images for article %s', url)

    # save images
    for image_url in article_parser.get_image_urls():
        image = get_image_from_url(image_url)
        filename = image_url.split('/')[-1]
        with (article_path / filename).open('wb') as fi:
            fi.write(image)

    logger.info('Finished downloading article %s', url)


def fetch_urls(num_threads: int, num_articles: int) -> List[str]:
    num_pages = num_articles // settings.ARTICLES_PER_PAGE + 1
    urls = []

    with typer.progressbar(length=num_pages, label='Fetching urls') as progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(get_article_urls_from_page, page)
                for page in range(1, num_pages + 1)
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    urls.extend(future.result())
                except RequestException as e:
                    typer.echo(f'Failed to fetch urls for articles: {e}', err=True)
                finally:
                    progress.update(1)

    return urls[:num_articles]


def download_articles(num_threads: int, article_urls: List[str], path: Path) -> None:
    with typer.progressbar(length=len(article_urls), label='Downloading') as progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_url = {
                executor.submit(save_article, url, path): url for url in article_urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except RequestException as e:
                    typer.echo(
                        f'Failed to download article with url {url}: {e}', err=True
                    )
                finally:
                    progress.update(1)


def save_articles(num_threads: int, num_articles: int, path: Path) -> None:
    typer.echo('Fetching urls for articles')
    article_urls = fetch_urls(num_threads, num_articles)
    typer.echo('Starting downloading articles...')
    download_articles(num_threads, article_urls, path)
    typer.echo('Finished downloading articles')
