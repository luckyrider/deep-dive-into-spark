nohup hive --service hiveserver2 --hiveconf hive.log4j.file=$HIVE_CONF_DIR/hive-hiveserver2-log4j.properties >$HIVE_HOME/hive-hiveserver2.out 2>&1 &
