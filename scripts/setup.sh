sudo apt-get update
sudo apt-get install -y git python-pip python-dev supervisor

mkdir florent && cd florent && git init
git pull https://$GITHUB_ACCESS_TOKEN@github.com/sihrc/florent-server.git

chmod og+X /root
sudo apt-get install -y build-essential postgresql postgresql-contrib libpq-dev
sudo service postgresql start
sudo -u postgres createuser -s florent
sudo -u postgres psql -c "ALTER USER florent WITH PASSWORD 'florentrocks';"

python setup.py develop
sudo cp supervisor.conf /etc/supervisord.conf
sudo service supervisor start
