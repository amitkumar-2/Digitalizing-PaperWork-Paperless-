# syntax=docker/dockerfile:1

#FROM python:3.8-slim-buster

#WORKDIR /python-docker

#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt

#COPY . .

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


####################################################################################

FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./main.py