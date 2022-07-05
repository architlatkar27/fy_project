var config_server = {
    _id: "rs-config-server",
    configsvr: true,
    version: 1,
    members: [ 
        { _id: 0, host : 'configsvr01:27017' },
        { _id: 1, host : 'configsvr02:27017' },
        { _id: 2, host : 'configsvr03:27017' },
        { _id: 3, host : 'configsvr04:27017' },
        { _id: 4, host : 'configsvr05:27017' },
        { _id: 5, host : 'configsvr06:27017' },
        { _id: 6, host : 'configsvr07:27017' },
        // { _id: 7, host : 'configsvr08:27017' },
        // { _id: 8, host : 'configsvr09:27017' },
    ]
};

var status_config_server = rs.initiate(config_server);

printjson(status_config_server);
