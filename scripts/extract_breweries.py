import requests
import json
import os
from datetime import datetime

def run():
    url = "https://api.openbrewerydb.org/v1/breweries?per_page=50"
    response = requests.get(url)

    

    if response.status_code == 200:
        data = response.json()

        bronze_dir = "/opt/airflow/data_lake/bronze"
        os.makedirs(bronze_dir, exist_ok=True)
        filename = os.path.join(bronze_dir, f"breweries_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json")
        with open(filename, "w") as f:
            json.dump(data,f)

        print(f"Dados salvos com sucesso em: {filename}")
    else:
        print(f"Erro ao acessar API: {response.status_code}")
    
if __name__ == "__main__":
    run()