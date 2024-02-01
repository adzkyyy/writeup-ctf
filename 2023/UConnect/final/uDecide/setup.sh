sudo docker rm -f udecide

sudo docker build -t udecide .

sudo docker run --name udecide -d -it -p 10003:10003 udecide