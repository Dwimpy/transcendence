FROM python:3.11.6-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat openssl
WORKDIR /server

COPY . .

RUN pip install -r requirements.txt
RUN mkdir -p /certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/django.key -out /certs/django.crt -subj "/CN=localhost"
RUN chmod +x ./start_server.sh

EXPOSE 443

CMD ["./start_server.sh"]