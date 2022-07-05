var config_replicaset_08 = {
    _id: "rs-shard-08",
    version: 1,
    members:[
        { _id: 0, host : "shard08-a:27017" },
        { _id: 1, host : "shard08-b:27017" },
        { _id: 2, host : "shard08-c:27017" }, 
    ]
};

var status_replicaset_08 = rs.initiate(config_replicaset_08);

printjson(status_replicaset_08);
