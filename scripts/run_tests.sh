#!/usr/bin/env bash

# testing code with
docker run --name $1 -v $2:/tmp/$3 python:3.5.2-alpine python /tmp/$3

# cleaning up
docker rm $1 > /dev/null
