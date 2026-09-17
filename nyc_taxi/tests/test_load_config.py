import pytest

from nyc_taxi.src.utils.config.load_config import load_config


def test_load_config_invalid_environment():
    with pytest.raises(ValueError, match="Environnement 'invalid' absent"):
        load_config("variable_environnement", "invalid")


