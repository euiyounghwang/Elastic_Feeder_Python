
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
