FROM python:3.10-slim

WORKDIR /app

COPY proxy.py /app/

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "proxy.py"]
