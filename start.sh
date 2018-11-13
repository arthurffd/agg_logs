#!/bin/sh
now=$(date +"%T")
echo "Calling application LogAggMuti: $now"
#python LogAggMulti.py
python3 LogAggMulti.py
echo "Application LogAggMuti terminated: $now"