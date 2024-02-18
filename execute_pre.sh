#!/bin/bash

python3 multiprocess.py &
sleep 3
python3 ./lib/AIWolf/pre/connect_to_server.py