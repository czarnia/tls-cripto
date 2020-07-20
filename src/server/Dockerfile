FROM python:3.7-alpine
RUN apk add python3-dev build-base --update-cache
RUN pip3 install pycrypto
COPY ./ /src
WORKDIR /src/server
