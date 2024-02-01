sudo docker rm -f usystemv2

sudo docker build -t usystemv2 .

sudo docker run --restart always --name usystemv2 -d -it -p 10001:10001 usystemv2