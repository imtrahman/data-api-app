FROM public.ecr.aws/docker/library/python:3.9.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update &&\
 apt-get install -y curl &&\
 pip install -r requirements.txt

CMD [ "python",  "main.py"]
