var config_replicaset_09 = {
    _id: "rs-shard-09",
    version: 1,
    members:[
        { _id: 0, host : "shard09-a:27017" },
        { _id: 1, host : "shard09-b:27017" },
        { _id: 2, host : "shard09-c:27017" }, 
    ]
};

var status_replicaset_09 = rs.initiate(config_replicaset_09);

printjson(status_replicaset_09);
