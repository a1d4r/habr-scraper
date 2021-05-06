from pathlib import Path

import pytest
from typer.testing import CliRunner

from app.main import app
from app.utils import to_valid_filename

runner = CliRunner()


@pytest.mark.usefixtures('mock_habr')
def test_app(tmp_path: Path):
    dirname = to_valid_filename('Кто помнит «старшего брата» CD и DVD? / Хабр')
    result = runner.invoke(app, ['--articles', '1', '--path', str(tmp_path)])

    assert result.exit_code == 0
    assert 'Done' in result.stdout
    assert (tmp_path / dirname).exists()
    assert (tmp_path / dirname / 'article.txt').exists()
