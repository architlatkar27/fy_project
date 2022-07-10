Fully sharded mongo environment using docker-compose and local storage.

Tree based sharding:
The MongoDB environment consists of the following docker containers

router0X: Mongo routing service to connect to the cluster through (2 containers)
configsvr0X: Stores metadata for sharded data distribution
shard0X-Y: Mongod data server with three replica sets containing 3 nodes each (9 shards)
mongoexpressX: UI for routing service

mongosX: Mongod data server with three replica sets containing 3 nodes each (9 shards)
mongoexpressX: UI for each shard
main_node: The algorithm on flask server (bind mount for live changes)


Default mongo sharding(hashing):
The MongoDB environment consists of the following docker containers

mongosX: Mongod data server with three replica sets containing 3 nodes each (9 shards)
mongoexpressX: UI for each shard
main_node: The algorithm on flask server

Docker Swarm setup:
(Change the env variables, docker container configs accordingly)

- Instructions for 4 nodes (including a storage node) docker swarm setup:

	1. get.docker.com .. install docker on all VMs (run both commands under "This script is meant for the quick & easy installation")
	2. ssh into all VMs with sudo access (or add docker usergroup) 
	3. Run "docker swarm init" on the leader node.
	4. Run "docker swarm join-token manager", copy paste the output to all other VMs, so that all other nodes will be added to the swarm as manager.
	5. To confirm all the nodes present in swarm, run "docker node ls"
	6. Create a common network (attachable) among all nodes on the swarm using "docker network create --driver overlay --attachable dedupe"
	7. To confirm, run "docker network ls" on all the VMs and check the scope(==swarm) and driver(==overlay)
	8. Build and push the image "docker-compose build", "docker-compose push".
	8. Pull the image for dedupe nodes separately "docker image pull abhishekvtangod/xyz"
	9. Pull the image for cloud node "docker image pull abhishekvtangod/xyz"

	10. Run the containers on all VMs.
		- docker container run -d --name node1 --network appName --env PYTHONUNBUFFERED=1 --env node_id=1 -p 5001:5000 --hostname localhost abhishekvtangod/abc
		- docker container run -d --name node2 --network appName --env PYTHONUNBUFFERED=1 --env node_id=2 -p 5002:5000 --hostname localhost abhishekvtangod/abc
		- docker container run -d --name node3 --network appName --env PYTHONUNBUFFERED=1 --env node_id=3 -p 5003:5000 --hostname localhost abhishekvtangod/mno
		- docker container run -d --name main_node --network appName --env PYTHONUNBUFFERED=1 -p 5000:5000 --hostname localhost abhishekvtangod/pqr

	11. Access all the urls from individual ips of VM with appropriate ports(change port mappings according to your ease and avoid confusions).




How to run native_shard?

Init:

```bash
Run the containers:
docker-compose up -d

Initialize config servers:
bash bash/init-configserver.sh

Initialize shards: 
bash bash/init-replicaset.sh 

After initializing config servers and shards, wait a bit to elect primaries before initializing router:
bash bash/init-router.sh 

```

Verify Status:


```bash
before checking the status verify if all the containers are up:
docker container ls

status of replica:
docker exec -it shard-01-node-a bash 
Inside VM: mongo
Mongo shell: rs.status()

status of router:
docker-compose exec router01 mongo --port 27017
Inside mongo shell:  sh.status()
```

Enable sharding and partition key for the DB:
```bash
sh.enableSharding('my_db');
sh.shardCollection('my_db.people',{'age':"hashed"});
```


Clean up:
```bash
bash clean_all.sh 
```