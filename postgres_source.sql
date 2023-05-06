CREATE SOURCE CONNECTOR `postgres-src-01` WITH(
    "connector.class"='io.confluent.connect.jdbc.JdbcSourceConnector',
    "connection.url"='jdbc:postgresql://postgres:5432/quiz02_dev?user=root&password=secret',
    "mode"='incrementing',
    "incrementing.column.name"='index',
    "topic.prefix"='',
    "table.whitelist"='quiz02_raw',
    "key"='index');