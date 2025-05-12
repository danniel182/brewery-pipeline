from pyspark.sql import SparkSession 
import os 
os.environ["PYSPARK_PYTHON"] = "/usr/local/bin/python"

def run():
    #usando o config para resolver o problema de bloqueio de recursos pelo Security Maneger do macOS
    spark = SparkSession.builder \
    .appName("Transform Breweries v1") \
    .config("spark.driver.extraJavaOptions", "--add-opens java.base/java.lang=ALL-UNNAMED") \
    .getOrCreate()

    bronze_dir = "/opt/airflow/data_lake/bronze"
    files = sorted([f for f in os.listdir(bronze_dir) if f.endswith(".json")])
    if not files:
        print ("Nenhum arquivo encontrado na camada bronze")
        return

    latest_file = os.path.join(bronze_dir, files[-1])

    df = spark.read.json(latest_file)

    #verifica se o dataframe tem dados disponíveis
    if df.count() == 0:
        raise ValueError("O DataFrame está vazio. Verifique a camada bronze.")
    
    #selecionando campos relevantes (alguns tem semantica duplicada)
    df_selected = df.select(
        "id", "name", "brewery_type", "city",
        "state_province", "country", "postal_code",
        "website_url", "phone", "longitude", "latitude"
    )

    #remover linhas com dados críticos ausentes
    df_clean = df_selected.dropna(subset=["id", "name", "brewery_type", "state_province","country"])

    #escrita como Parquet, particionando por estado
    silver_dir = "/opt/airflow/data_lake/silver/breweries"
    os.makedirs(silver_dir, exist_ok=True)
    df_clean.write.mode("overwrite").partitionBy("state_province").parquet(silver_dir)

    print(f"Dados transformados e salvos em: {silver_dir}")
    spark.stop()

if __name__ == "__main__":
    run()