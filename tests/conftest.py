import json
import re

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses


@pytest.fixture(scope='session')
def habr_html():
    with open('test_data/habr.html') as f:
        yield f.read()


@pytest.fixture(scope='session')
def article_html():
    with open('test_data/article.html') as f:
        yield f.read()


@pytest.fixture(scope='session')
def article_urls():
    with open('test_data/article_urls.json') as f:
        yield json.load(f)


@pytest.fixture(scope='session')
def image_urls():
    with open('test_data/image_urls.json') as f:
        yield json.load(f)


@pytest.fixture(scope='session')
def image():
    with open('test_data/image.jpg', 'rb') as f:
        yield f.read()


@pytest.fixture(scope='session')
def article_text_fragments():
    with open('test_data/article_text_fragments.json') as f:
        yield json.load(f)


@pytest.fixture(scope='session')
def mock_habr(habr_html: str, image: bytes, article_html: str):
    with aioresponses() as m:
        m.get(re.compile(r'https://habr.com/page\d+'), body=habr_html, repeat=True)
        m.get(
            re.compile(r'https://habr.com/\w+/(company|post)/\S+'),
            body=article_html,
            repeat=True,
        )
        m.get(re.compile(r'https://habrastorage.org/\S+'), body=image, repeat=True)
        yield


@pytest.fixture()
async def client_session():
    async with ClientSession() as session:
        yield session
