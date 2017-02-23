FROM klaemo/couchdb:2.0.0
# Clean original build artefacts and install Python query server
RUN rm -rf /etc/apt/sources.list.d/*
RUN apt-get update -y -qq && apt-get install -y python-couchdb
# Enable Python query server
COPY couchpy.ini /opt/couchdb/etc/local.d/
