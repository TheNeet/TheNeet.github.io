#!/bin/sh

file_size=()
file_name=()
num=5
if [ -z $1 ]; then
	filename=$(cd `dirname $0`; pwd)
elif [[ $1 == "-n" && $3 == "-d" ]]; then
	filename="$4"
	num=$2
else 
	echo "usage: ./file_size.sh [-n N] [-d DIR]"
	echo "Show top N largest files/directories"
	exit
fi

size() {
	m=$num
	n=`ls -l "$1" | awk '{ print $5 }'`
	for ((i=num-1;i>=0;--i));
	do
		if [ $n -gt ${file_size[$i]} ]; then
			file_size[$i+1]=${file_size[$i]}
			file_name[$i+1]=${file_name[$i]}
			m=$i
		fi
	done
	file_size[$m]=$n
	file_name[$m]=$1
}

#递归获得改文件夹下所有子文件的 name ，调用 size 函数比较大小
filecheck() {
	local name="$1/"
	for file in `ls "$1"`
	do
		name="$name$file"
		if [ -d "$name" ] || [ -f "$name" ]; then
                        if [ -d "$name" ]; then 
                                filecheck "$name"
                        else 
                                size "$name"
                        fi   
			name="$1/"
		else      
			name="$name "
		fi
	done
}
#初始化，否则会报错
for ((i=0;i<num;++i))
do
	file_size[$i]=0
done
#调用函数
filecheck "$filename"
#输出
for ((i=0;i<num;++i))
do
	printf "%d\t%d\t%s\t\n" $(($i + 1)) ${file_size[$i]} "${file_name[$i]}"
done
