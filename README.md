# FLASK-STEPPER-CONTROL

Flask api that will control stepper over raspberry pi

## Run flask on local network

```flask run --host=0.0.0.0```

## Build docker DEV image:

```docker build -f Dockerfile --platform linux/arm/v7 -t ognjetina/flask-stepper-control:dev .```

## Run flask from docker

```docker run --privileged -p 5000:5000 ognjetina/flask-stepper-control:dev```

### Build docker PRODUCTION image:

```docker build -f Dockerfile --platform linux/arm/v7 -t ognjetina/flask-stepper-control:production .```

### Push docker image:

```docker push ognjetina/flask-stepper-control:production```

# Startup services on raspberry pi

- Step 1 - Create file `flask-stepper-control.service` in `/etc/systemd/system/`
- Step 2 - Give permission to file: `sudo chmod 644 flask-stepper-control.service`
- Step 3 - Make systemd see your service `sudo systemctl flask-stepper-control.service`

File example:

```
[Unit]
Description=Flaprivilegedsk Stepper controler
Requires=docker.service
After=docker.service

[Service]
TimeoutStartSec=0
ExecStart=/usr/bin/docker run -a STDOUT --privileged --rm -p 5000:5000 --name flask-stepper-control ognjetina/flask-stepper-control:production 
ExecStop=/usr/bin/docker stop -t 2 ognjetina/flask-stepper-control:production

[Install]
WantedBy=default.target
```
