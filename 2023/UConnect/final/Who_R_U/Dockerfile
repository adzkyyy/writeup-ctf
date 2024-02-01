FROM ubuntu:20.04

RUN apt-get update && apt-get -y install socat gcc gcc-multilib

COPY service /service
WORKDIR /service

RUN chmod 555 whoru

EXPOSE 10002
USER nobody

CMD socat -v tcp-l:10002,reuseaddr,fork exec:'./whoru'
