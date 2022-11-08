FROM python:3

WORKDIR /usr/src/video-server

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "server.py" ]