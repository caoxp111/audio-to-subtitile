FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04-python310

USER root
WORKDIR /app/content-extract
COPY . .

VOLUME /app/content-extract/out-puts
VOLUME /app/content-extract/models
VOLUME /app/content-extract/upload

RUN mkdir logs

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]