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

## Importing documents

With elasticdump-like output file:
```
python3 utils/import.py path/to/elasticdump.json -u username -p password -e http://endpoint:port -d declarations -c 8 -C 1500
```
This will run import in 8 processes of 1500 chunks max per each concurrently against the "declarations" CouchDB database at specified endpoint with corresponding credentials with the dump as a first argument. Additionally `-P` option may be used to purge the DB prior to import.


## Adding views with map/reduce functions

Reference functions (currently only `map` stage) are available in `data/reference` directory in this repository.

In order to add a function (and create a design document for it) please use the following helper script:
```
python3 utils/addview.py data/reference/income_map_function.coffee -u username -p password -d declarations -D reference -v read_income -l coffeescript
```
This will create a "reference" design document on the "declarations" DB with a "read_income" view, containing a map function provided in `data/reference/income_map_function.coffee` file, compiling it from CoffeeScript on the fly.

Supported `-l` (language) values are currently "javascript" (for the default couchjs/SpiderMonkey), "chakra" (for couch-chakra/ChakraCore), which supports ES6 natively and "coffeescript" (transpiles into ES5 and runs on couchjs). Benchmark docker image also allows "python", "pypy" and "erlang".

TODO: Create a Dockerfile for utils.

## Exporting views

Currently exporting views to CSV files is supported using the following script:
```
python3 utils/export.py ddoc_name view_name -u username -p password -o /path/to/output.csv
```
However, it's currently somewhat hardcoded to the view functions from `views/`. See `utils/export.py` for more details.


## Benchmarking

`addview.py` script supports benchmarking mode, which initiates a view query for the added/updated view and tracks CouchDB's active indexing tasks, logging performance metrics. In order to utilise it pass `-b` argument.

**Note**: Benchmarking with CouchDB is a little nuanced since it never really deletes things (unless you tell it) and therefore in some cases it might happen that only a part of shards (or even none) are going to be indexed. Please make sure you're using fresh design documents for benchmark runs, which have *never* been used before even if deleted. Alternatively compact the design docs, delete them and run views cleanup before reusing.

Another point to keep in mind is having your DB volume on the host side to avoid docker storage overhead as well as avoiding the loop device as docker's storage engine.

For convenience there's a Dockerfile for benchmarking various query servers in `couchdb/benchmark`, which depends on "dragnet/couchdb" image to be present.

I've written a detailed article about [benchmarking CouchDB views](https://medium.com/@excieve/benchmarking-couchdb-views-abb7a0a891b2) using this project and our dataset. But here's some quick results of functions from `data/reference` run over a dataset of ≈300000 real-world documents with a nested structure.

Using ES6 with `chakra` language ([couch-chakra](https://github.com/dmunch/couch-chakra) query server utilising ChakraCore JS runtime):

```
INFO:dragnet.addview:average = 1237.26c/s (all_tasks) 154.38c/s (one task)
INFO:dragnet.addview:total time = 241s
```

Using the default ES5 couchjs (SpiderMonkey JS runtime under the hood):
```
INFO:dragnet.addview:average = 1193.69c/s (all_tasks) 148.37c/s (one task)
INFO:dragnet.addview:total time = 247s
```

Using CPython (`python` language):
```
INFO:dragnet.addview:average = 1316.64c/s (all_tasks) 163.34c/s (one task)
INFO:dragnet.addview:total time = 223s
```

Using PyPy (`pypy` language):
```
INFO:dragnet.addview:average = 1055.33c/s (all_tasks) 132.30c/s (one task)
INFO:dragnet.addview:total time = 282s
```

Using JS (SpiderMonkey) transpiled from CoffeeScript (`coffeescript` language):
```
INFO:dragnet.addview:average = 1214.11c/s (all_tasks) 151.64c/s (one task)
INFO:dragnet.addview:total time = 242s
```

Using native Erlang query server (quite likely not the best function quality out there affected it a bit):
```
INFO:dragnet.addview:average = 1391.36c/s (all_tasks) 174.55c/s (one task)
INFO:dragnet.addview:total time = 213s
```

TODO: jq (when there's a proper query server for it).


