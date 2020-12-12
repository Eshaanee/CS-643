#!/bin/bash
workdir="/usr/app"
#workdir=$PWD
$workdir/spark/bin/spark-submit --conf "spark.driver.extraJavaOptions=-Dlog4jspark.root.logger=WARN,console" $workdir/testerD115.py $workdir/rfwine_model.model  $@ 2>/dev/null
