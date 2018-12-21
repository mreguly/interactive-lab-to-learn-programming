#!/usr/bin/env bash

# run docker container
docker run --name $1 -v $2:/tmp/$1 python:3.5.2-alpine python /tmp/$1

# remove container after finish
docker rm $1 > /dev/null