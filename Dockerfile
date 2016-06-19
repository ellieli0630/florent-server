FROM phusion/baseimage

RUN apt-get update && \
    apt-get install -y git python python-pip python-dev && \
    apt-get install -y build-essential postgresql postgresql-contrib libpq-dev && \
    pip install supervisor && \
    pip install tornado psutil pyzmq futures decorator SQLAlchemy psycopg2

RUN sudo service postgresql start && \
    sudo -u postgres createuser -s florent && \
    sudo -u postgres psql -c "ALTER USER florent WITH PASSWORD 'florentrocks';"

ADD . /florent
WORKDIR /florent

RUN cp supervisord.conf /etc/supervisord.conf && \
    python setup.py develop

CMD ["supervisord"]
