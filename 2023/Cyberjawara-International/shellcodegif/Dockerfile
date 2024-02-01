FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc -y
RUN apt-get install socat -y

RUN useradd --create-home --shell /bin/bash flag
COPY build/flag.txt /home/flag/flag.txt
COPY build/readFlag /home/flag/readFlag
RUN chmod 555 /home/flag/
RUN chmod 400 /home/flag/flag.txt
RUN chown flag:flag /home/flag/flag.txt /home/flag/readFlag
RUN chmod +s /home/flag/readFlag

RUN useradd --create-home --shell /bin/bash ctf
COPY build/challenge /home/ctf/challenge
WORKDIR /home/ctf

RUN chmod 555 challenge

CMD socat TCP-LISTEN:3001,reuseaddr,fork EXEC:"./challenge",su=ctf && fg