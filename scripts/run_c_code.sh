#!/usr/bin/env bash

# run docker container
docker run --rm --name $1 -v $3:/tmp frolvlad/alpine-gcc gcc --static /tmp/$4 -o /tmp/$5

#docker rm $1 > /dev/null