# Brewery Data Pipeline 🍺

Este projeto implementa um pipeline de dados usando **Apache Spark** para processamento, orquestrado com **Apache Airflow**, e gerenciado em containers via **Docker Compose**. A fonte de dados é a [Open Brewery DB API](https://www.openbrewerydb.org/).

---

## 🔧 Requisitos Mínimos

Para rodar o projeto, você precisa ter:

- Docker (>= 20.10)
- Docker Compose (>= 1.29)
- 4 GB de RAM disponíveis
- Internet ativa (para chamadas à API)

---

## 📁 Estrutura de Diretórios

```bash
.
├── dags/                       # DAG do Airflow
├── data_lake/
│   ├── bronze/                 # Dados brutos extraídos
│   ├── silver/                 # Dados transformados
│   └── gold/                   # Dados agregados
├── scripts/                    # Scripts PySpark de ETL
├── logs/                       # Logs do Airflow
├── plugins/                   # Plugins customizados (opcional)
├── requirements.txt           # Dependências do projeto
├── .devcontainer/Dockerfile   # Imagem base customizada
└── docker-compose.yml         # Arquitetura dos serviços

Como Rodar o Projeto
✅ Opção 1 – Rodar o pipeline manualmente (sem Airflow)
Execute cada etapa isoladamente usando:

# no bash
docker compose build -d
#Isso iniciará: estrutura de container do docker para realização das tarefas
docker compose run spark-runner-extract
docker compose run spark-runner-transform
docker compose run spark-runner-aggregate
# Os resultados serão salvos localmente nas pastas data_lake/bronze, silver e gold.

Opção 2 – Subir o Airflow e orquestrar tudo via DAG
1. Inicie os serviços
#bash
docker compose up --build -d
#Isso iniciará: PostgreSQL, Redis, Airflow Webserver, Scheduler e Worker.

2. Acesse a interface do Airflow
Abra o navegador e acesse:
👉 http://localhost:8080

Credenciais:

Usuário: admin
Senha: admin

3. Rode a DAG
Localize a DAG etl_brewery.

Clique em "Trigger DAG" (botão de ▶️).

Acompanhe os logs clicando nas tarefas: extract, transform, aggregate.

🧪 Scripts e Componentes
Todos estão em scripts/:

extract_breweries.py: coleta dados da API e salva em bronze/

transform_breweries.py: limpa, seleciona e salva dados em silver/

aggregate_breweries.py: cria agregações por estado e cidade e salva em gold/

📂 Airflow DAG
Arquivo: dags/brewery_pipeline.py
Executa os 3 scripts na ordem correta com BashOperator.

📦 Dependências Instaladas
As principais dependências estão no requirements.txt:

apache-airflow[celery,postgres]==2.7.3
pyspark
psycopg2-binary
requests
flask-session

O ambiente é baseado em python:3.9 e openjdk para suporte ao Spark.

🧪 Testes e Tratamento de Erros (Em construção)
Scripts incluem verificações de status da API, existência de diretórios e arquivos.

Logs são registrados automaticamente via Airflow.

Diretório tests/ contém scripts com testes simples de verificação das funções principais.

Para rodar testes (dentro de um container com pytest instalado):

docker compose run airflow-worker pytest
🔔 Monitoramento e Alertas (visão futura)
Para um ambiente de produção, recomenda-se configurar:

Alertas por e-mail via Airflow em falhas de DAG.

Verificações de qualidade de dados antes de salvar arquivos.

Ferramentas externas como Prometheus + Grafana para monitorar tempo de execução e falhas.

📝 Contribuições
Sinta-se livre para abrir issues, sugerir melhorias ou criar pull requests. É um projeto aberto para aprendizados e melhorias contínuas.

🛠️ Dicas e Comandos Úteis
bash
Copy
# Acompanhar os containers em tempo real
docker compose logs -f

# Subir Airflow manualmente com worker, scheduler e webserver
docker compose up airflow-webserver airflow-scheduler airflow-worker

# Remover containers órfãos
docker compose down --remove-orphans

# Acessar um container para debug
docker exec -it <nome-do-container> bash