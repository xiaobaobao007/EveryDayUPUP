#ulimit -c unlimited

CUR_PATH=`pwd`;

MainClass=com.intion.GameServer
JAVA_OPTS="-Xdebug  -Xrunjdwp:transport=dt_socket,address=9808,server=y,suspend=n -server -Xmx1024m -Xms1024m -Xmn256m -XX:MaxPermSize=32m -Djava.awt.headless=true -Xverify:none -Dfile.encoding=UTF8"
#JAVA_OPTS="-server -Xmx1024m -Xms1024m -Xmn256m -XX:MaxPermSize=32m -Djava.awt.headless=true -Xverify:none -Dfile.encoding=UTF8"
PID_FILE=server.pid

. ./psutil.sh

#判断进程是否已经启动
check_running
if [ $? -eq 1 ]
then
	echo "server is already running!!!!!!!"
	exit 1
fi

declare -A simple_name_version
declare -A full_version_name

for i in libs/*.jar
do
  if [ "${i:5:4}" == "qun-" ]
  then
    v=${i%.jar*}
    v=${v##*.}

    key=${i:5:10}

    if [ ! -n "${simple_name_version[$key]}" ]
    then
      simple_name_version[$key]=$v
      full_version_name[$key]=$i
    else
      let a=${simple_name_version[$key]}
      let b=$v
      if [ $a -lt $b ]
      then
        simple_name_version[$key]=$v
        full_version_name[$key]=$i
      fi
    fi

	else
	  p_classpath=$i:"$p_classpath"
	fi

done

for key in ${!full_version_name[*]}
do
  p_classpath=${full_version_name[$key]}:"$p_classpath"
done

$JAVA_HOME/bin/java  $JAVA_OPTS  -classpath $p_classpath:resources $MainClass >stout.log 2>&1 &

PID=$!;
#判断是否启动成功
sleep 2
check_process $PID
if [ $? -eq 1 ] ; then
	echo -e "Starting Server .................\033[0;32;1m[OK]\033[0m"
else
	echo -e "Starting Server .................\033[0;31;1m[FAIL]\033[0m"
	exit 1
fi

echo $PID > $PID_FILE