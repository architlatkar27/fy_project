Fully sharded mongo environment using docker-compose and local storage.


The MongoDB environment consists of the following docker containers

mongosrs(1-3)n(1-3): Mongod data server with three replica sets containing 3 nodes each (9 containers)
mongocfg(1-3): Stores metadata for sharded data distribution (3 containers)
mongos(1-2): Mongo routing service to connect to the cluster through (1 container)
