FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]