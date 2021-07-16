#!/usr/bin/env zsh
source ~/anaconda3/bin/activate alm # replace with own conda environment

pushd ../../backend
python app.py
