sudo docker rm -f unotev2

sudo docker build -t unotev2 .

sudo docker run --restart always --name unotev2 -d -it -p 10005:10005 unotev2