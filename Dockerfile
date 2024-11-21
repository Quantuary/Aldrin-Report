# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .
CMD ["python", "apprun.py"]