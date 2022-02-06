#!/bin/bash

rm -rf apk-extracted
python3 ./apktool/apktool.py --apktool ./apktool/apktool_2.6.0.jar $1 >> ./analysis_output/general/$2.txt
