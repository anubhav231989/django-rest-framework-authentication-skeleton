#BASE IMAGE.
FROM python:3.8-alpine

#TAG THE IMAGE WITH MAINTAINER NAME & EMAIL.
LABEL Maintainer-Name="Anubhav Sidhu"
LABEL Maintainer-Email="anubhav231989@gmail.com"

#SET ANY ENV VARIABLES NEEDED.
ENV PYTHONUNBUFFERED 1

#UPDATE BASE IMAGE.
RUN apk update

#INSTALL OS-LEVEL APPLICATION DEPENDENCIES.
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers

#COPY APPLICATION DEPENDENCIES.
COPY ./dependencies.txt /dependencies.txt

#INSTALL APPLICATION DEPENDENCIES.
RUN pip install -r /dependencies.txt

#DELETE ANY TEMPORARY OD-LEVEL DEPENDENCIES (IF ANY).
RUN apk del .tmp-build-deps

#CREATE AND SET WORKING DIRECTORY.
RUN mkdir /source
WORKDIR /source

#COPY SOURCE CODE.
COPY ./source /source

#EXPOSE PORTS.

#DEFAULT CONTAINER COMMAND.