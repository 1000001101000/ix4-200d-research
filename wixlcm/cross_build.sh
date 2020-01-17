#!/bin/bash

##requires build-essential, linux-source, etc

tar xf "/usr/src/$(ls /usr/src/ | grep linux-source)"

make CROSS_COMPILE="arm-linux-gnueabi-" KERNEL_SOURCE="$(ls | grep linux-source)" all

make kernelversion
