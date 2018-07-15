#!/bin/sh

Usage() {
        echo "usage: ./self_compression.sh [--list] or [Source compressed file] [Destination path]"
        echo "Self compression according to the file name suffix"
        exit         
}

Hint() {
        echo "Supported file types: zip tar tar.gz tar.bz2"                  
        exit
}

Tar()  {
        tar xvf "$file" -C "$filepath"
        exit
}

if [ "$1" == "--list" ]; then
	Hint
elif ! [ -z "$1" ]; then
	#获取压缩包位置
	file="$1"
	if ! [ -f "$file" ]; then
		Usage
	fi
	#获取解压位置
	filepath=$(cd `dirname $0`; pwd)
	if ! [ -z "$2" ]; then
		filepath="$2"
	fi
	if ! [ -d "$filepath" ]; then
		mkdir "$filepath"
	fi
	#解压操作
	mold=${file:0-3:3}
	echo "$mold"
	if [ $mold == zip ]; then
		unzip "$file" -d "$filepath"
		exit
	elif [ $mold == tar ]; then
		Tar
	fi
	mold=${file:0-6:6}
	if [ $mold == tar.gz ]; then
		Tar
	fi
	mold=${file:0-7:7}
	if [ $mold == tar.bz2 ]; then
		Tar
	fi
	Hint
else
	Usage
fi
