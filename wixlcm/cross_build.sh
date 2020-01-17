#!/bin/bash

##requires build-essential, linux-source, etc

tar xf "/usr/src/$(ls /usr/src/ | grep linux-source)"
if [ "$?" -ne 0 ]; then
   exit 1
fi

cd "$(ls | grep linux-source)" 
kver="$(make kernelversion)"
echo $kver
cd -

echo $(pwd)
#make CROSS_COMPILE="arm-linux-gnueabi-" KERNEL_SOURCE="$(ls | grep linux-source)" all >/dev/null 2>&1
if [ "$?" -ne 0 ]; then
   exit 1
fi

mkdir -p "bins/$kver/" 2>/dev/null

cp wixlcm.ko "bins/$kver/"

find .

