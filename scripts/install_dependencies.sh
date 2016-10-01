#!/bin/bash

echo 'installing dependencies'
cd /home/ubuntu/ParkingFinder/

virtualenv /tmp/ParkingFinder/env

. /tmp/ParkingFinder/env/bin/activate

pip install -r requirements.txt
