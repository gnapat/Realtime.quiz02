CREATE SINK CONNECTOR `elasticsearch-sink-all-01` WITH(
    "connector.class"='io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
    "connection.url"='http://elasticsearch:9200',
    "connection.username"='',
    "connection.password"='',
    "batch.size"='1',
    "write.method"='insert',
    "topics"='quiz02_all',
    "type.name"='changes',
    "value.converter.schema.registry.url" ='http://schema-registry.quiz02:8081',
    "value.converter" = 'io.confluent.connect.avro.AvroConverter',
    "key.ignore" = 'true',
    "key"='index');