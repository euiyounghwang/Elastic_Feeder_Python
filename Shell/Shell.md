
## Authentication BatchJob Shell

```sh
echo "#######################################"
	
if [ "$1" = "start" ] ; then
	echo "Start Redis Process !!"
	nohup /WAS/DATA/ES/AuthorizationServer/execute.sh 8180 /dev/null 2>&1 &
	nohup /WAS/DATA/ES/AuthorizationServer/execute.sh 8182 /dev/null 2>&1 &
	nohup /WAS/DATA/ES/AuthorizationServer/execute.sh 8184 /dev/null 2>&1 &
	nohup /WAS/DATA/ES/AuthorizationServer/execute.sh 8186 /dev/null 2>&1 &
elif [ "$1" = "stop" ] ; then
	echo "Stop Redis Process !!"
	kill -9 $(ps aux |awk '/AuthorizationServer/ {print $2}')

else
	echo "input excute parameter. (start or stop)"

echo "#######################################"

ps -ef | grep AuthorizationServer
```

## DELETE BatchJob Shell

```sh
#!/bin/ksh

RESULT=`curl -H 'Content-Type: application/json' -u 'elastic:gsaadmin' -XPOST 'http://10.132.57.75:9205/ict_sop_idx/_delete_by_query' -d '
{
  "query": {
    "match_all": {}
  }
}
'`

echo $RESULT
```


## EXECUTE BatchJob Shell

```sh
#!/bin/ksh
clear

echo "######################################"
echo "####                              ####"
echo "####  START  AuthorizationServer  ####"
echo "####                              ####"
echo "######################################"
echo "================================================"

export LANG=ko_KR.UTF-8
export JAVA_HOME=/usr/local/jdk1.6.0_33/bin
export RUN_JAR=/WAS/DATA/ES/AuthorizationServer/AuthorizationServer.jar

echo "> LANG : $LANG"
echo "> JAVA_HOME : $JAVA_HOME"
echo "> RUN_JAR : $RUN_JAR"


$JAVA_HOME/java -classpath $RUN_JAR -jar $RUN_JAR $1
```


## FeedClients BatchJob Shell

```sh
#!/bin/ksh
clear

#export LD_LIBRARY_PATH=./lib/lib_linux64:$LD_LIBRARY_PATH
#export LIBPATH=./lib/lib_linux64:$LIBPATH
#export CLASSPATH=.:./lib/fasoo-jni-2.7.6u.jar:$CLASSPATH

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/TOM/DrmDocFilter
export LIBPATH=$LIBPATH:/TOM/DrmDocFilter
export CLASSPATH=/TOM/DrmDocFilter/libfasoopackager.so:/TOM/DrmDocFilter/fasoo-jni-2.7.6u.jar:.

echo "###################################"
echo "####                           ####"
echo "####    START  GSA  FEEDS!     ####"
echo "####                           ####"
echo "###################################"
echo "================================================"

RUN_JAR=/WAS/DATA/ES/Feeds/ElasticMDL.jar

echo ">URN_JAR : $RUN_JAR"

export RUN_JAR
export LANG=ko_KR

echo ">LANG : $LANG"


#echo "----<<<< feedJob.sh  BATCH  START!!!! >>>>----"
echo "----<<<< [$1] [$2] SYSTEM  BATCH  START!!!! >>>>----"
echo "========================================================="


#echo "---- START Start.java [`date +%T`]----"
echo "----START [$1] [$2] SYSTEM [`date +%T`]----"
start=`date +%T`
s_start=`perl -e 'print time()'`
t_start=`perl -e 'print time()'`
#/TOM/jdk1.8.0_131/bin/java -classpath /WAS/DATA/ES/Feeds/ElasticMDL.jar -jar   /WAS/DATA/ES/Feeds/ElasticMDL.jar  $1 $2
/TOM/jdk1.8.0_171/bin/java -classpath /WAS/DATA/ES/Feeds/ElasticMDL.jar -jar   /WAS/DATA/ES/Feeds/ElasticMDL.jar  $1 $2
s_end=`perl -e 'print time()'`
#echo "---- END   Start.java [`date +%T`]----"
echo "----END   [$1] [$2] SYSTEM [`date +%T`]----"
echo "----[$1] [$2] SYSTEM ??? ?? : [ `expr $s_end - $s_start`?? ]----"
echo "---------------------------------------------------------"

end=`date +%T`
t_end=`perl -e 'print time()'`

#echo "----<<<< feedJob.sh  BATCH  END!!!! >>>>----"
echo "----<<<< [$1] [$2] SYSTEM  BATCH  END!!!! >>>>----"
echo "----??? ???? ?? : [$start]----"
echo "----??? ???? ?? : [$end]----"

#t_start=1336960472
#t_end=1336960572

minus=`expr $t_end - $t_start`
share=`expr $minus / 60`
rest=`expr $minus % 60`

if [ $minus -ge 60 ]
then
        #echo $share $rest
        #echo `expr $share`?? `expr $rest`??
        #echo $share ?? $rest ??
	echo "----???? ?? ??? ?? : [ `expr $share`?? `expr $rest`?? ]----"
else
	echo "----???? ?? ??? ?? : [ `expr $minus`?? ]----"
fi
#echo "----???? ?? ??? ?? : [ `expr $t_end - $t_start`?? ]----"

echo "========================================================="
echo "###################################"
echo "####                           ####"
echo "####    END  GSA  FEEDS!       ####"
echo "####                           ####"
echo "###################################"

```

## LogStash BatchJob Shell

```sh

echo "#############################################"
echo "#       Authorization Log Crawling          #" 
echo "#############################################"

nohup /WAS/DATA/ES/logstash-5.6.10/bin/logstash -f /WAS/DATA/ES/logstash-5.6.10/logstash_auth_logs.conf  > /dev/null &
echo "# Crawling Start.....                       #"


#for port in 8180 8182 8184 8186
#do
#	nohup /TOM/logstash-5.2.0/bin/logstash -f /TOM/logstash-5.2.0/logstash_authz_$port.conf  > /dev/null &
#    echo "# [$port] Crawling Start                     #"
#done

echo "#############################################"

```



