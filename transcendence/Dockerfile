FROM python:3.11.6-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat
WORKDIR /server

COPY . .

RUN pip install -r requirements.txt
RUN chmod +x ./start_server.sh

CMD ["./start_server.sh"]
