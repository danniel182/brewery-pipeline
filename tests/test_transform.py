from pyspark.sql import SparkSession
import pytest
import os

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local[1]").appName("Test").getOrCreate()

def test_transform_columns_exist(spark):
    df = spark.read.json("tests/mocks/sample_breweries.json")  # mock de entrada
    columns_esperadas = {"id", "name", "state_province"}

    for col in columns_esperadas:
        assert col in df.columns
