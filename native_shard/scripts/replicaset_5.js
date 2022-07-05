var config_replicaset_05 = {
    _id: "rs-shard-05",
    version: 1,
    members:[
        { _id: 0, host : "shard05-a:27017" },
        { _id: 1, host : "shard05-b:27017" },
        { _id: 2, host : "shard05-c:27017" }, 
    ]
};

var status_replicaset_05 = rs.initiate(config_replicaset_05);

printjson(status_replicaset_05);
