import asyncio
import time
from pathlib import Path

import typer

from app import settings
from app.scraper import save_articles

app = typer.Typer()


@app.command()
def main(
    articles: int = typer.Option(...),
    path: Path = settings.DESTINATION_DIRECTORY,
) -> None:
    """Save articles from habr.com"""
    typer.echo('Starting...')
    start = time.time()
    asyncio.run(save_articles(articles, path))
    elapsed = time.time() - start
    typer.echo(f'Done in {elapsed :.2f} seconds')


if __name__ == '__main__':  # pragma: no cover
    app()
