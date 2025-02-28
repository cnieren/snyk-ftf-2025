FROM python:3.9-slim

ENV MYSQL_ROOT_PASSWORD=yourpassword
ENV MYSQL_DATABASE=blog_db

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    default-libmysqlclient-dev \
    build-essential \
    mariadb-server mariadb-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY flag.txt .

EXPOSE 5000

COPY app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
