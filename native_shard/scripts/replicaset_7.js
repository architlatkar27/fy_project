var config_replicaset_07 = {
    _id: "rs-shard-07",
    version: 1,
    members:[
        { _id: 0, host : "shard07-a:27017" },
        { _id: 1, host : "shard07-b:27017" },
        { _id: 2, host : "shard07-c:27017" }, 
    ]
};

var status_replicaset_07 = rs.initiate(config_replicaset_07);

printjson(status_replicaset_07);
