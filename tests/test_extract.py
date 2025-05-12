import os
import pytest
from scripts import extract_breweries

def test_extract_creates_file(tmp_path):
    # Substitui a criação real de arquivos com pasta temporária
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    extract_breweries.run()

    bronze_dir = tmp_path / "/opt/airflow/data_lake/bronze"
    arquivos = list(bronze_dir.glob("*.json"))
    assert len(arquivos) == 1

    os.chdir(original_dir)

def test_extract_api_error(monkeypatch):
    # Simula erro na API
    import requests
    def fake_get(*args, **kwargs):
        class FakeResponse:
            status_code = 500
            def json(self): return {}
        return FakeResponse()
    monkeypatch.setattr(requests, "get", fake_get)
    
    with pytest.raises(Exception):
        extract_breweries.run()