FROM ubuntu:20.04

RUN apt-get update && apt-get -y install socat gcc gcc-multilib

COPY service /service
WORKDIR /service

RUN chmod 555 uNotev2

EXPOSE 10005
USER nobody

CMD socat -v tcp-l:10005,reuseaddr,fork exec:'./uNotev2'
