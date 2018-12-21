#!/usr/bin/env bash

# run docker container
#docker run --name $1 -v $2:/tmp/$1 python:3.5.2-alpine python /tmp/$1
#docker run --rm --name $1 -v $3:/tmp frolvlad/alpine-gcc gcc --static /tmp/test.c -o /tmp/test

#echo $3
#echo $4
#echo $5

docker run --rm -v $3:/tmp -w /tmp java:alpine javac /tmp/$4

docker run --rm -v $3:/tmp -w /tmp java:alpine java $5

#docker rm $1 > /dev/null



