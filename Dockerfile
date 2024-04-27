FROM ubuntu:20.04
FROM python:alpine
LABEL authors="bubo"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver"]