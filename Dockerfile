# syntax=docker/dockerfile:1
FROM python
WORKDIR /code
COPY . .

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
# TODO: Test this
RUN apt update && apt install -y chromium-driver

ENTRYPOINT ["sh", "./run.sh"]

