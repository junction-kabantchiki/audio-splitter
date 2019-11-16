FROM python:3.7

RUN \
  apt-get update && \
  apt-get install -y \
    libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python-pyaudio ffmpeg

WORKDIR /app/
COPY . /app/

RUN \
  pip install \
    -r model/requirements.txt \
    -r splitter/requirements.txt \
    -r requirements.txt

ENV PYTHONPATH "/app/model:/app/splitter:${PYTHONPATH}"
EXPOSE 5000
CMD python /app/app.py
