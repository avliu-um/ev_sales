# syntax=docker/dockerfile:1
FROM python
WORKDIR code/ 
RUN pip3 install --upgrade pip
#RUN git clone https://github.com/avliu-um/asian_yelp.git
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY test_runner.py test_runner.py
COPY run.sh run.sh

ENTRYPOINT ["sh", "./run.sh"]

