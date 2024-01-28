FROM python:3.11.6-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir Django

WORKDIR /Django
COPY ./transcendence .
COPY ./transcendence/tools/start_server.sh .

RUN pip install -r requirements.txt
RUN chmod +x ./start_server.sh

CMD ["./start_server.sh"]