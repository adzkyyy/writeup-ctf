sudo docker rm -f whoru

sudo docker build -t whoru .

sudo docker run --restart always --name whoru -d -it -p 10002:10002 whoru