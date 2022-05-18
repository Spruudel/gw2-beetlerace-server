FROM python:3.9

WORKDIR /usr/src/ws_server
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
CMD [ "python", "./start_server.py" ]
