FROM public.ecr.aws/docker/library/python:3.9.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update &&\
 apt-get install -y curl &&\
 pip install -r requirements.txt &&\
 opentelemetry-bootstrap --action=install

ENV OTEL_PROPAGATORS=xray 
ENV OTEL_PYTHON_ID_GENERATOR=xray

CMD [ "opentelemetry-instrument", "python",  "main.py"]