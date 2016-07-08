installation

dependencies:

nltk:
sudo pip install -U nltk
sudo python -m nltk.downloader -d /usr/local/share/nltk_data all

practNLPtools:
git clone https://github.com/biplab-iitb/practNLPTools
cd practNLPTools
sudo python setup.py install

Editing rules:
Edit rules.json file. See this file for example rules
