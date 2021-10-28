CUR_PATH=`pwd`

check_running()
{
	# echo "CHECK PID_FILE:$PID_FILE"
	if ! [ -f $PID_FILE ]
	    then
	    # echo "no pid file!"
	    return 0
	fi
	
	PID=`cat $PID_FILE`
	if [ -z $PID ] ; then
		return 0
	fi
	
	check_process $PID
	PROC_RUNNING=$?
	if [ $PROC_RUNNING -eq 0 ]
	then
	    # echo "process not exist, rm pid file!"
	    rm -rf $PID_FILE
	    return 0
	else
	    return 1
	fi
}


check_process()
{
	if [ $# -ne 1 ] || [  -z $1 ] ; then
         return 0
    fi
    return `ps -p $1 --no-header | wc -l`
}
