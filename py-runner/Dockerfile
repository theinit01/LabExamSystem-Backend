FROM python:3.10-slim

WORKDIR /app

RUN pip install Flask

COPY . .

EXPOSE 5000

CMD ["python3", "code-p.py"]