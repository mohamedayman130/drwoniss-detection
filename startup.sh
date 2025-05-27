#!/bin/bash

APP_DIR="/home/site/wwwroot"

cd $APP_DIR

apt-get update && apt-get install -y libgl1-mesa-glx

source antenv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000
