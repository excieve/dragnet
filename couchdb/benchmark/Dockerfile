# Implies dragnet/couchdb image is built and available
FROM dragnet/couchdb
# Install python2, pypy and Python query server in addition to the others
RUN apt-get install -y python python-pip && pip install couchdb
RUN curl -fSL https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.6-linux_x86_64-portable.tar.bz2 -o /usr/src/pypy-5.6-linux_x86_64-portable.tar.bz2 &&\
    tar -xjf /usr/src/pypy-5.6-linux_x86_64-portable.tar.bz2 -C /opt/ && ln -s /opt/pypy-5.6-linux_x86_64-portable /opt/pypy
RUN rm -rf /usr/src/*
RUN /opt/pypy/bin/pypy -m ensurepip && /opt/pypy/bin/pip install couchdb
COPY benchmark.ini /opt/couchdb/etc/local.d/
