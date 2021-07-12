FROM python:3.8-slim

COPY requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

VOLUME ["/app"]

WORKDIR /app
CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "coffee.wsgi:app"]
