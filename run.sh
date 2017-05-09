#! /bin/bash

CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
dataset=$1
ITERS=100

for i in $(seq 1 100)
do
    for f in $(find $CDIR/datasets/$dataset -name *.tim)
    do
        echo "$CDIR/main.py -i $f -o $(echo $f | sed -e "s@\.tim@__$i\.sln@g") > $(echo $f | sed -e "s@\.tim@__$i\.log@g") 2>&1"
    done
done
