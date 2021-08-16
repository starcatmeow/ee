#!/bin/bash
# Use this script to upscale 8x8 accurately

if [ -z "$1" ]
then
	echo "Need an input!!!!!"
	exit
fi


convert "$1" -filter point -resize 10000% ${1%.*}\ upscaled.png
