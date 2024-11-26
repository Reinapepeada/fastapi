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
py -m venv venv
```

## Usage
```
venv\Scripts\activate
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

# FastAPI Example

This example starts up a [FastAPI](https://fastapi.tiangolo.com/) server.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-NvLj4?referralCode=CRJ8FE)
## ✨ Features

- FastAPI
- [Hypercorn](https://hypercorn.readthedocs.io/)
- Python 3

## 💁‍♀️ How to use

- Clone locally and install packages with pip using `pip install -r requirements.txt`
- Run locally using `hypercorn main:app --reload`

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- To learn about Hypercorn and how to configure it, read their [Documentation](https://hypercorn.readthedocs.io/)
