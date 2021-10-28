declare -A simple_name_version
declare -A full_version_name

for i in libs/*.jar
do
  if [ "${i:5:5}" == "qun-g" ]
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
  echo ${full_version_name[$key]}
  p_classpath=${full_version_name[$key]}:"$p_classpath"
done