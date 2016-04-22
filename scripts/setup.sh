sudo apt-get update
sudo apt-get install -y git python-pip python-dev supervisor

mkdir florent && cd florent && git init
git pull https://$GITHUB_ACCESS_TOKEN@github.com/sihrc/florent-server.git

python setup.py develop
sudo cp supervisor.conf /etc/supervisord.conf
sudo service supervisor start
