cd florent-server

curl -fsSL https://get.docker.com/ | sh

sudo apt-get update
sudo apt-get install -y git
git clone https://$GITHUB_ACCESS_TOKEN@github.com/sihrc/florent-server.git

sudo docker build -t florent-docker .
sudo docker run -d -v /var/lib/postgresql/9.3/main -p 0.0.0.0:80:80 -t florent-docker &
