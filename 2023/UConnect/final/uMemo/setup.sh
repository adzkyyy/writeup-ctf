sudo docker rm -f umemo

sudo docker build -t umemo .

sudo docker run -d -it -p 10004:10004 umemo