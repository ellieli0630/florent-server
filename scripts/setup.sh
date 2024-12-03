cd ~
chmod og+X ~

curl -fsSL https://get.docker.com/ | sh

sudo apt-get update

git clone https://$GITHUB_ACCESS_TOKEN@github.com/sihrc/florent-server.git
