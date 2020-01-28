#!/bin/bash

##requires build-essential, linux-source, etc

tar xf "/usr/src/$(ls /usr/src/ | grep linux-source)"
if [ "$?" -ne 0 ]; then
   exit 1
fi

source_dir="$(ls | grep linux-source)"

cd "$source_dir" 
cfg_file="$(find /usr/src/linux-config-* | grep armel_none_marvell | grep xz)"
xzcat "$cfg_file" > .config
kver="$(make kernelversion)"
echo $kver
cd -

echo $(pwd)
make CROSS_COMPILE="arm-linux-gnueabi-" KERNEL_SOURCE="$source_dir" all
if [ "$?" -ne 0 ]; then
   exit 1
fi

mkdir -p "bins/$kver/" 2>/dev/null
cp -v wixlcm.ko "bins/$kver/"
rm -r "$source_dir"

find .

