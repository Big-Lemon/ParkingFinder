#!/bin/bash
export CLAY_CONFIG='config/development.json'
if [ "$DEPLOYMENT_GROUP_NAME" == "Test" ]
then
	export CLAY_CONFIG='config/test.json'
fi
cd /home/ubuntu/ParkingFinder

. /tmp/ParkingFinder/env/bin/activate

python serve.py > /dev/null 2> /dev/null < /dev/null &
