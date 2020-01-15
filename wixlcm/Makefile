CROSS_COMPILE ?=
KERNEL_SOURCE ?=

obj-m += wixlcm.o

all:
	make ARCH=arm CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SOURCE) M=$(PWD) scripts prepare
	make ARCH=arm CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SOURCE) M=$(PWD) mvebu_v5_defconfig
	make ARCH=arm CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SOURCE) M=$(PWD) modules

clean:
	make ARCH=arm CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SOURCE) M=$(PWD) clean
