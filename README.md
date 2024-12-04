---
title: FastAPI
description: A FastAPI server
tags:
  - fastapi
  - hypercorn
  - python
---

## Installation
```
py -m venv .venv
```

## Usage
```
.venv\Scripts\activate
```

## install dependencies
```
pip install -r requirements.txt


## Run for development
```
fastapi dev main.py 
```
or 

## Run for production << si vas a correr dos microservicios a la vez aclara el puerto "--port xxxx">>
```
fastapi run main.py
```
```
<!-- incicio rapido -->
 py -m .venv venv ;.venv\Scripts\activate;pip install -r requirements.txt;fastapi dev main.py

```
# Migrar base de datos a postgress cuando se cambia algo en el modelo
##Inicializar Alembic: En el directorio raíz de tu proyecto, ejecuta:
alembic init alembic

Esto creará un directorio alembic y un archivo alembic.ini.

## Configurar Alembic: Configura tu varibal de entorno de DATABASE_URL
DATABASE_URL = "postgresql://user:password@localhost/dbname"


## Crear una migración: Cada vez que realices cambios en tus modelos, crea una nueva migración:
alembic revision --autogenerate -m "Descripción de los cambios"

Esto generará un nuevo archivo de migración en el directorio alembic/versions.

## Aplicar la migración: Para aplicar la migración a la base de datos, ejecuta:
alembic upgrade head
alembic downgrade -1
Esto aplicará la migración a la base de datos y actualizará la tabla alembic_version para reflejar la migración aplicada.


## 💁‍♀️ How to use

- Clone locally and install packages with pip using `pip install -r requirements.txt`
- Run locally using `hypercorn main:app --reload`

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- To learn about Hypercorn and how to configure it, read their [Documentation](https://hypercorn.readthedocs.io/)


