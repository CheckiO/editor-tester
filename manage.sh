#!/bin/sh

SCRIPTPATH=$( cd "$( dirname "$BASH_SOURCE" )" && pwd )

VOLUMES="-v $SCRIPTPATH/editor_tester:/opt/editor_tester"
VOLUMES=$VOLUMES" -v $SCRIPTPATH/tests_data:/opt/tests_data"
IMAGE="checkio/editor-tester"

case "$1" in
'build')
echo "Build new image"
docker build -t $IMAGE ./
;;
'run')
echo "Runing tests"
docker run -i -t $VOLUMES $IMAGE $2 $3 $4
;;
esac
