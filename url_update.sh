#!/bin/bash
rm -f underwater/url.txt
touch url.txt
for filename in underwater/*; do
	echo "https://github.com/shadySource/DATA/raw/master/underwater"+"$filename" >> url.txt
done
mv url.txt underwater/
