FROM python:3.10-slim

WORKDIR /app

RUN pip install Flask flask-cors

COPY . .

EXPOSE 5000

CMD ["python3", "code-p.py"]