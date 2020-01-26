#!/usr/bin/python3

import os
import time

RS = 15
A0 = 34
CS = 35
RW = 44
E  = 45
#DATA = [36,37,38,39,40,41,42,43]
DATA = [43,42,41,40,39,38,37,36]

A0_DATA = 0x01
A0_CMD  = 0x00

gpio_root = '/sys/class/gpio/'

def prep_gpio(pin):
	pin_dir = os.path.join(gpio_root,"gpio"+str(pin))


	if not os.path.exists(pin_dir):
		with open(os.path.join(gpio_root,'export'),'w') as f:
			f.write(str(pin))
			f.flush()
			f.close()

	if not os.path.exists(pin_dir):
		print("export failed")
		return -1

	with open(os.path.join(pin_dir,'direction'),'w') as f:
		f.write("out")
		f.flush()
		f.close()

	set_gpio(pin,0)

def close_gpio(pin):
        with open(os.path.join(gpio_root,'unexport'),'w') as f:
                f.write(str(pin))
                f.flush()
                f.close()

def set_gpio(pin,value):
	pin_dir = os.path.join(gpio_root,"gpio"+str(pin))
	if value == 0:
		outval = 0
	else:
		outval = 1

	with open(os.path.join(pin_dir,'value'),'w') as f:
		#print(outval,end = '')
		f.write(str(outval))
		f.flush()
		f.close()

	#print(" ",end = '')


def write_lcm(A0type, input):
	#print(hex(input)," ",end = '')
	mask=128
	set_gpio(E,0)
	for pin in DATA:
		set_gpio(pin,(input & mask))
		mask=int(mask/2)
	#print(" ",end = '')
	set_gpio(A0,A0type)
	#print(" ",end = '')
	#time.sleep(30/1000000.0)
	#udelay(30);
	set_gpio(RW,0)
	set_gpio(CS,0)
	set_gpio(E,1)
	#time.sleep(100/1000000.0)
	#udelay(100);
	set_gpio(E,0)
	set_gpio(CS,1)
	#time.sleep(100/1000000.0)
	#udelay(100);
	#print(" ")

def init_lcm():
	prep_gpio(RS)
	prep_gpio(CS)
	prep_gpio(RW)
	prep_gpio(A0)
	prep_gpio(E)

	for x in DATA:
		prep_gpio(x)
	set_gpio(RS,1)
	#print(" ")

	for x in [0xae,0xa2,0xa0,0xc8,0xa6,0x40,0x22,0x81,0x3f,0xf8,0x00,0xa4,0x2c]:
		write_lcm(A0_CMD,x)

	#time.sleep(0.2) #200ms?
	write_lcm(A0_CMD,0x2e)
	#time.sleep(0.2) #200ms?
	write_lcm(A0_CMD,0x2f)
	#time.sleep(0.4) #400ms?
	write_lcm(A0_CMD,0xaf);

def exit_lcm():
	close_gpio(RS)
	close_gpio(CS)
	close_gpio(RW)
	close_gpio(A0)
	close_gpio(E)

	for x in DATA:
		close_gpio(x)

def draw_lcm():
	write_lcm(A0_CMD,0xae)
	for page in range(8):
		write_lcm(A0_CMD,(0xB0 + page))
		write_lcm(A0_CMD,0x10)
		write_lcm(A0_CMD,0x00)
		for line in range(128):
			write_lcm(A0_DATA, 0xF0)
	write_lcm(A0_CMD,0xaf)

init_lcm()
draw_lcm()
#for x in range(200):
#	write_lcm(A0_CMD,0xA7)
#	time.sleep(1)
#	write_lcm(A0_CMD,0xA6)
#	time.sleep(1)

exit_lcm()
