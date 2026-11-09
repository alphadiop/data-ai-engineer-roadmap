
from unittest.mock import patch

from nyc_taxi.src.utils.config.normalize_path import normalize_path


def test_normalize_windows_path_on_linux():
    path = r"D:\data-ai-engineer-roadmap\nyc_taxi\data"

    with patch("nyc_taxi.src.utils.config.normalize_path.platform.system", return_value="Linux"):
        result = normalize_path(path, "local")

    assert result == "/mnt/d/data-ai-engineer-roadmap/nyc_taxi/data"


def test_linux_path_is_unchanged():
    path = "/mnt/d/data-ai-engineer-roadmap/nyc_taxi/data"

    with patch("nyc_taxi.src.utils.config.normalize_path.platform.system", return_value="Linux"):
        result = normalize_path(path, "local")

    assert result == path


def test_databricks_path_is_unchanged():
    path = r"D:\data-ai-engineer-roadmap\nyc_taxi\data"

    with patch("nyc_taxi.src.utils.config.normalize_path.platform.system", return_value="Linux"):
        result = normalize_path(path, "databricks")

    assert result == path


def test_windows_path_is_unchanged_on_windows():
    path = r"D:\data-ai-engineer-roadmap\nyc_taxi\data"

    with patch("nyc_taxi.src.utils.config.normalize_path.platform.system", return_value="Windows"):
        result = normalize_path(path, "local")

    assert result == path
