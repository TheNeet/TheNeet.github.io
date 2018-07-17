#!/bin/sh

factorial() {
	if [ $1 == 1 ]; then
		return 1
	fi
	sum=$(($1 - 1))
	factorial $sum
	sum=$(($sum * $1))
}

num=$1
if [ -z "$(echo $1 | sed 's#[0-9]##g')" ] && ! [ -z $1 ]; then
	factorial $num
	echo $sum
else 
	echo "usage: ./factorial.sh [N]"
	echo "calculate a number's factorial"
fi

