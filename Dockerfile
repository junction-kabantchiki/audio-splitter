FROM alfg/ffmpeg:latest

COPY . /app
WORKDIR /app
#RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apt install build-deps gcc libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python-pyaudio
RUN pip install --upgrade pip
RUN sh install.sh
EXPOSE 5000
CMD python ./app.py
