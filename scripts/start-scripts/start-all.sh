#!/usr/bin/env zsh

./startMongo.sh &
./startBackend.sh &
./startFrontend.sh &
