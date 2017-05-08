#! /bin/bash

CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
dataset=$1

for f in $(find $CDIR/datasets/$dataset -name *.tim)
do
	echo "$CDIR/main.py -i $f > $(echo $f | sed -e 's@\.tim@\.log@g') 2>&1"
done
