from pyspark.sql import SparkSession
from pyspark.sql.functions import count, when, col, countDistinct, desc
import time 
import os 
    
def run():

    spark = SparkSession.builder \
        .appName("Aggregate breweries v1") \
        .getOrCreate()
    
    #leitura da camada silver
    silver_path = "/opt/airflow/data_lake/silver/breweries"

    # Aguarda até o diretório existir
    timeout = 60  # segundos
    elapsed = 0
    while not os.path.exists(silver_path):
        time.sleep(2)
        elapsed += 2
        if elapsed > timeout:
            raise TimeoutError(f"Timeout: {silver_path} não encontrado após {timeout} segundos.")

    df = spark.read.parquet(silver_path)

    #verifica se o dataframe tem dados disponíveis
    if df.count() == 0:
        raise ValueError("O DataFrame está vazio. Verifique a camada silver.")

    #colunas auxiliares has_website e has_phone
    df = df.withColumn("has_website", when(col("website_url").isNotNull(), 1).otherwise(0)) \
           .withColumn("has_phone", when(col("phone").isNotNull(), 1).otherwise(0))

    #1. agregacao de contagem por estado e por tipo, incluindo dados como, quantas delas tem website
    #quantas tem telefone, e número de cidades por estado.
    agg_state_type = df.groupBy("state_province","brewery_type").agg(
        count("id").alias("brewery_count"),
        count(when(col("has_website") == 1 , True)).alias("with_website"),
        count(when(col("has_phone") == 1 , True)).alias("with_phone"),
        countDistinct("city").alias("unique_cities")
    )
    #escrita em camada gold
    output_byState = "/opt/airflow/data_lake/gold/aggregatedByState"
    os.makedirs(output_byState, exist_ok=True)
    agg_state_type.write.mode("overwrite").partitionBy("state_province").parquet(output_byState)

    #2. agregacao por top cidades com mais cervejarias
    agg_top_cities = df.groupBy("state_province","city").agg(
        count("id").alias("breweries_count")) \
        .orderBy(desc("breweries_count"))
    
    #escrita em camada gold
    output_byTopCity = "/opt/airflow/data_lake/gold/aggregatedByTopCity"
    os.makedirs(output_byTopCity, exist_ok=True)
    agg_top_cities.write.mode("overwrite").partitionBy("state_province").parquet(output_byTopCity)

    print(f"Camada Gold salvas em: {output_byState}, {output_byTopCity}")
    spark.stop()

if __name__ == "__main__":
    run()