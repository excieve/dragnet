# dragnet

## Running CouchDB

Build the docker image, from couchdb directory run:
```
sudo docker build -t dragnet/couchdb .
```

Run the container for that image:
```
sudo docker run -d -p 5984:5984 --name dragnet_couchdb dragnet/couchdb
```

This will run a CouchDB single node instance with Python Query Server on port 5984 in the "admin party mode", thus requires initial setup by accessing Fauxton in your browser on [localhost:5984/_utils/](http://localhost:5984/_utils/).


The container has a docker volume for the DB at `/opt/couchdb/data`, which can be mapped to any location on the host by launching it like this:
```
sudo docker run -d -p 5984:5984 --name dragnet_couchdb -v /some/path/on/host:/opt/couchdb/data dragnet/couchdb
```
