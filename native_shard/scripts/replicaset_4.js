var config_replicaset_04 = {
    _id: "rs-shard-04",
    version: 1,
    members:[
        { _id: 0, host : "shard04-a:27017" },
        { _id: 1, host : "shard04-b:27017" },
        { _id: 2, host : "shard04-c:27017" }, 
    ]
};

var status_replicaset_04 = rs.initiate(config_replicaset_04);

printjson(status_replicaset_04);
