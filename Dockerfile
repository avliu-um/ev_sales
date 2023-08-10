# syntax=docker/dockerfile:1
FROM python
WORKDIR /code 
RUN pip3 install --upgrade pip
#RUN git clone https://github.com/avliu-um/asian_yelp.git
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./run.sh"]

