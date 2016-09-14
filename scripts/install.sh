# Install scripts to setup a clean Linux Ubuntu 14.04 LTS machine to production-ready state

# Install Docker
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates python-pip
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo mkdir -p /etc/apt/sources.list.d/
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee -a /etc/apt/sources.list.d/docker.list
sudo apt-get update && sudo apt-get purge lxc-docker && sudo apt-cache policy docker-engine

sudo apt-get install -y linux-image-extra-$(uname -r)
sudo apt-get install -y apparmor docker-engine
sudo service docker start

# Setup Script
GITHUB_ACCESS_TOKEN="8ab7faff3584999a2c4dc25b0d92e715261b736b"
mkdir florent && cd florent && git init
git pull https://$GITHUB_ACCESS_TOKEN@github.com/sihrc/florent-server.git

# Build Docker
sudo docker build -t florent-server .
sudo docker run -d -t florenet-server
