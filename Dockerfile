FROM phusion/baseimage

ADD . /florent-server
WORKDIR /florent-server

RUN apt-get update -q && \
    apt-get install -y wget git build-essential python27 python-setuptools python-dev python-pip && \
    pip install supervisor && \
    cp ./scripts/supervisord.conf /etc/supervisor/supervisord.conf

CMD ["/usr/bin/supervisord"]
