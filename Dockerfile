FROM arm32v7/python:3-alpine

WORKDIR /app

EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]