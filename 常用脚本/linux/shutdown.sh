CUR_PATH=`pwd`;

PID_FILE=server.pid

. ./psutil.sh

check_running
RET=$?
if [ $RET == 1 ]
then
        echo -n "Stopping Server "

        PID=`cat $PID_FILE`
        declare -i count
        count=0
        kill -15 $PID
        sleep 1
        check_process $PID
        RET=$?
        while [ "$RET" = "1" ] && [ $count -lt 60  ]
        do
                echo -n "."
                sleep 1
                check_process $PID
                RET=$?
                count=count+1
        done

        if [ $RET = 0 ]; then
                echo -e ".................\033[0;32;1m[Done]\033[0m"
				rm -f $PID_FILE
        else
                echo -e ".................\033[0;31;1m[FAIL]\033[0m"
        fi
else
        echo -e "Server IS Not Running!"
fi