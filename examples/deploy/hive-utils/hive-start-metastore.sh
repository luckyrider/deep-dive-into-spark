nohup hive --service metastore --hiveconf hive.log4j.file=$HIVE_CONF_DIR/hive-metastore-log4j.properties >$HIVE_HOME/hive-metastore.out 2>&1 &
