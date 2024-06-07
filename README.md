# TCA Kedro Pipelines

## Overview

Pipelines para el procesamiento de datos del proyecto Booking Patterns (clustering). \
La pipeline culmina ingestando las diferentes tablas generadas a un azure blob storage donde desde aquí pueden ser accesados por el dashboard de streamlit.

## Instalar dependencias
```
pip install -r requirements.txt
```

## Prerequisitos
- Datos
    - Reservaciones dataset (TCA)
    - Canales dataset (TCA)
    - Agencias dataset (TCA)
- Azure
    Incluir en credentials.yml los siguientes datos de tu cuenta azure:
    - account_name
    - [account_key](https://stackoverflow.com/questions/61706239/retrieve-blob-storage-connection-string-using-az-cli-or-python-sdk)

    Así mismo, incluir el nombre de tu contenedor de Azure Cloud Storage Account:
    - container_name

## Como correr la pipeline
A la altura del root del directorio
```
kedro run
```

## Como visualizar la pipeline
A la altura del root del directorio
```
kedro viz run
```
