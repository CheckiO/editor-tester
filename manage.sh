#!/bin/sh

SCRIPTPATH=$( cd "$( dirname "$BASH_SOURCE" )" && pwd )

VOLUMES="-v $SCRIPTPATH/tests:/opt/project/tests"
IMAGE="checkio/editor-tester"

case "$1" in
'build')
echo "Build new image"
docker build -t $IMAGE ./
;;
'run-tests')
echo "Runing tests"
docker run -i -t $VOLUMES $IMAGE
;;
esac
