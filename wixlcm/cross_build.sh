#!/bin/bash

##requires build-essential, linux-source, etc

tar xf "/usr/src/$(ls /usr/src/ | grep linux-source)"
cd "$(ls | grep linux-source)" make kernelversion
exit 0

make CROSS_COMPILE="arm-linux-gnueabi-" KERNEL_SOURCE="$(ls | grep linux-source)" all


