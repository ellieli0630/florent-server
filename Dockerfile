FROM phusion/baseimage

RUN apt-get update && \
    apt-get install -y git python python-pip python-dev && \
    apt-get install -y build-essential postgresql postgresql-contrib libpq-dev && \
    pip install supervisor

RUN sudo service postgresql start && \
    sudo -u postgres createuser -s florent && \
    sudo -u postgres psql -c "ALTER USER florent WITH PASSWORD 'florentrocks';"

ADD . /florent
WORKDIR /florent

RUN cp supervisord.conf /etc/supervisor/supervisord.conf && \
    python setup.py develop

CMD ["/usr/bin/supervisord"]
