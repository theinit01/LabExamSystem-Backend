FROM python:3.10-slim

WORKDIR /app

COPY proxy.py /app/

RUN pip install flask requests flask-cors

EXPOSE 8080

CMD ["python", "proxy.py"]
