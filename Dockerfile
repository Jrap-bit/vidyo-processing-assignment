FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y ffmpeg libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "videoprocessingapi.wsgi:application"]
