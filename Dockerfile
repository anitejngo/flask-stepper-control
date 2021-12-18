FROM arm32v7/python:3-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]