FROM apache/couchdb:2.3
# Clean original build artefacts and compile couch-chakra
RUN rm -rf /etc/apt/sources.list.d/* &&\
    echo 'deb http://ftp.debian.org/debian buster-backports main' >> /etc/apt/sources.list
RUN apt-get update -y -qq && apt-get install -y clang-3.8 cmake libunwind8 libunwind8-dev unzip libicu-dev
WORKDIR /usr/src
RUN curl -fSL https://github.com/Microsoft/ChakraCore/archive/cb7817bda7e4b265e7a7364641123e20204facfd.zip -o ChakraCore.zip &&\
    unzip ChakraCore.zip &&\
    curl -fSL https://github.com/dmunch/couch-chakra/archive/0c89ae7abe1a9e34aff54870540f7d3930a5671f.zip -o couch-chakra-unicode.zip &&\
    unzip couch-chakra-unicode.zip
WORKDIR /usr/src/ChakraCore-cb7817bda7e4b265e7a7364641123e20204facfd
RUN ./build.sh -j 4 --cxx=/usr/bin/clang++-3.8 --cc=/usr/bin/clang-3.8 &&\
    cp BuildLinux/Release/libChakraCore.so /usr/lib/
WORKDIR /usr/src/couch-chakra-0c89ae7abe1a9e34aff54870540f7d3930a5671f
RUN apt-get install -y vim-common
RUN make CHAKRA_INCLUDE_DIR="/usr/src/ChakraCore-cb7817bda7e4b265e7a7364641123e20204facfd/lib/Jsrt/" CHAKRA_LD_FLAGS="-L/usr/lib -lChakraCore" &&\
    mkdir /opt/couch-chakra && cp bin/couch-chakra /opt/couch-chakra/ &&\
    cat /opt/couchdb/share/server/main.js | sed 's/for each (fun in State.funs) {/State.funs.forEach(function(fun) {/g' | sed 's/print(JSON.stringify(buf));/); print(JSON.stringify(buf));/g' > /opt/couch-chakra/main.js
WORKDIR /opt/couchdb
RUN rm -rf /usr/src/*
ENV COUCHDB_QUERY_SERVER_CHAKRA "/opt/couch-chakra/couch-chakra /opt/couch-chakra/main.js"
COPY couch_chakra.ini /opt/couchdb/etc/local.d/
