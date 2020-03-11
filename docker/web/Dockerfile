FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY entrypoint.sh /usr/local/bin/

RUN apt-get update \
  && apt-get -y install cmake postgresql-client \
  && rm -r /var/lib/apt/lists/* \
  && apt-get clean

ENTRYPOINT ["entrypoint.sh"]
