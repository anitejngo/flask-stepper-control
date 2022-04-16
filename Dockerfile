FROM raspbian/stretch:latest

WORKDIR /app

EXPOSE 5000

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN sudo apt update
RUN sudo apt install locales python3 python3-pip -y


RUN pip3 install RPi.GPIO
RUN pip3 install Flask
RUN pip3 install rpimotorlib
RUN pip3 install flask-cors

COPY . /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]