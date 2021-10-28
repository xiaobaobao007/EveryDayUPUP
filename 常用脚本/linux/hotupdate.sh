#!/bin/sh

#windows下换行在linux会出现问题，用此命令修复
#sed -i 's/\r//g' hotupdate.sh

fileRoot=/data/main/gameserver/java_arthas/
for file in `ls $fileRoot`
do
  if [[ $file == *.java ]]
  then
    echo ${file%.java*} > java_arthas/0.txt

    ./arthas.sh <<EOF
sc -d *`cat java_arthas/0.txt` | grep classLoaderHash > java_arthas/1.txt
`head -n 1 java_arthas/1.txt > java_arthas/2.txt`
mc -c  `cut -d' ' -f5 java_arthas/2.txt` java_arthas/`cat java_arthas/0.txt`.java -d /java_arthas > java_arthas/3.txt
`sed -n '2,2p' java_arthas/3.txt > java_arthas/4.txt`
redefine `cat java_arthas/4.txt`
exit
EOF
    sleep 1
  fi
done