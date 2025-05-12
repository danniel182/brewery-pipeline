FROM apache/airflow:2.7.3-python3.9

USER root

# Atualiza pacotes e instala dependências
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-pip \
    libpq-dev \
    curl \
    default-jdk \
    procps \
    && apt-get clean

# Configurações de ambiente e permissões
ENV JAVA_HOME=/usr/
ENV PATH=$JAVA_HOME/bin:$PATH
ENV HOME=/opt/airflow
WORKDIR /opt/airflow

# Copia os requisitos
COPY requirements.txt /requirements.txt

# Define permissões para o diretório
RUN mkdir -p /opt/airflow/.ivy2/local && chmod -R 777 /opt/airflow

# Alterna para o usuário airflow
USER airflow

# Instala as dependências do Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt
