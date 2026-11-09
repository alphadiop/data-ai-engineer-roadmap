from unittest.mock import MagicMock
from types import SimpleNamespace

import pytest

from nyc_taxi.src.common.catalog_manager import CatalogManager


@pytest.fixture
def spark_mock():
    return MagicMock()


@pytest.mark.parametrize(
    "env, expected_schema",
    [
        ("local", "silver"),
        ("docker", "silver"),
        ("databricks", "nyc_taxi.silver"),
    ]
)
def test_table_exists_returns_true(
    spark_mock,
    env,
    expected_schema
):
    # Arrange
    spark_mock.sql.return_value.collect.return_value = [
        SimpleNamespace(tableName="silver_nyc_taxi"),
        SimpleNamespace(tableName="gold_fact_trips"),
    ]

    manager = CatalogManager(
        spark=spark_mock,
        logger=None,
        env=env
    )

    # Act
    result = manager.table_exists(
        catalog_name="nyc_taxi",
        schema_name="silver",
        table_name="silver_nyc_taxi"
    )

    # Assert
    assert result is True

    spark_mock.sql.assert_called_once_with(
        f"SHOW TABLES IN {expected_schema}"
    )


def test_table_exists_returns_false(spark_mock):
    # Arrange
    spark_mock.sql.return_value.collect.return_value = [
        SimpleNamespace(tableName="gold_fact_trips"),
    ]

    manager = CatalogManager(
        spark=spark_mock,
        logger=None,
        env="databricks"
    )

    # Act
    result = manager.table_exists(
        catalog_name="nyc_taxi",
        schema_name="silver",
        table_name="silver_nyc_taxi"
    )

    # Assert
    assert result is False

    spark_mock.sql.assert_called_once_with(
        "SHOW TABLES IN nyc_taxi.silver"
    )