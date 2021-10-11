FROM python:3.9-alpine

WORKDIR .

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual python3-dev
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "main.py"]