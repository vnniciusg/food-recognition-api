
FROM python:3.9-slim

#Instalar bibliotecas
COPY ./requirements.txt ./
RUN pip install -r requirements.txt && \
    rm ./requirements.txt

#Setup container directories
RUN mkdir /src
COPY ./src /src

WORKDIR /src
EXPOSE 8080

CMD ["gunicorn", "app:app", "--timeout=0", "--preload", \
    "--workers=1", "--threads=4", "--bind=0.0.0.0:8080"]