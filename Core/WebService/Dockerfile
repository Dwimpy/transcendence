FROM python:3.11.6-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir Django

WORKDIR /Django
COPY . .

RUN pip install -r requirements.txt
RUN pip install django-bootstrap-v5

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
