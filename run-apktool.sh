#!/bin/bash

rm -rf apk-extracted
python3 ./apktool/apktool.py --apktool ./apktool/apktool_2.6.0.jar $1 >> $2/$3.txt
