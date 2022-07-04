var config_replicaset_06 = {
    _id: "rs-shard-06",
    version: 1,
    members:[
        { _id: 0, host : "shard06-a:27017" },
        { _id: 1, host : "shard06-b:27017" },
        { _id: 2, host : "shard06-c:27017" }, 
    ]
};

var status_replicaset_06 = rs.initiate(config_replicaset_06);

printjson(status_replicaset_06);
