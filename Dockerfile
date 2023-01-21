FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app/src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

EXPOSE 8000

WORKDIR /app/src

CMD ["python", "crypto_api/__main__.py"]
