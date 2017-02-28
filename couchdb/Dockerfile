FROM klaemo/couchdb:2.0.0
# Clean original build artefacts and add R backports repo
RUN rm -rf /etc/apt/sources.list.d/* &&\
    echo 'deb http://www.stats.bris.ac.uk/R/bin/linux/debian jessie-cran3/' > /etc/apt/sources.list.d/rbackport.list && \
    apt-key adv --keyserver keys.gnupg.net --recv-key 6212B7B7931C4BB16280BA1306F90DE5381BA480
# Install Python3 and R packages
RUN apt-get update -y -qq && apt-get install -y python3 python3-dev python3-pip r-base r-base-dev
# Install fresh python-couchdb (with Python3 support) and rpy2
RUN pip3 install couchdb rpy2
# Install "jsonlite" lib for R
RUN Rscript -e 'install.packages("jsonlite",repos = "http://www.stats.bris.ac.uk/R")'
# Enable Python query server
COPY couchpy.ini /opt/couchdb/etc/local.d/
