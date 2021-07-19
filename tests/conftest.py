import json
import re

import pytest
from requests_mock import Mocker


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


@pytest.fixture()
def mock_habr(requests_mock: Mocker, habr_html: str, image: bytes, article_html: str):
    requests_mock.get(re.compile(r'https://habr.com/all/page\d+'), text=habr_html)
    requests_mock.get(
        re.compile(r'https://habr.com/\w+/(company|post)/\S+'), text=article_html
    )
    requests_mock.get(re.compile(r'https://habrastorage.org/\S+'), content=image)
