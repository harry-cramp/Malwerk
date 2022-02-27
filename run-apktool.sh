#!/bin/bash

rm -rf apk-extracted
python3 ./Malwerk/apktool/apktool.py --apktool ./Malwerk/apktool/apktool_2.6.0.jar $1 >> ./Malwerk/analysis_output/general/$2.txt
python3 ./Malwerk/feature-extractor.py ./Malwerk/analysis_output/general/$2.txt
