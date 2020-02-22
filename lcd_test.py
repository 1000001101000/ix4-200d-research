#!/usr/bin/python3

import os
from periphery import GPIO
from PIL import Image

RS = GPIO(15, "out")
A0 = GPIO(34, "out")
CS = GPIO(35, "out")
RW = GPIO(44, "out")
E = GPIO(45, "out")

D0 = GPIO(36, "out")
D1 = GPIO(37, "out")
D2 = GPIO(38, "out")
D3 = GPIO(39, "out")
D4 = GPIO(40, "out")
D5 = GPIO(41, "out")
D6 = GPIO(42, "out")
D7 = GPIO(43, "out")
DATA = [D7,D6,D5,D4,D3,D2,D1,D0]

A0_DATA = 0x01
A0_CMD  = 0x00

def set_gpio(pin,value):
	pin.direction = "out"
	if value == 0:
		outval = False
	else:
		outval = True
	pin.write(outval)

def read_gpio(pin):
	pin.direction = "in"
	if pin.read():
		return 1
	else:
		return 0

def write_lcm(A0type, input):
	mask=128
	set_gpio(E,0)
	for pin in DATA:
		set_gpio(pin,(input & mask))
		mask=int(mask/2)
	set_gpio(A0,A0type)
	set_gpio(RW,0)
	set_gpio(CS,0)
	set_gpio(E,1)
	set_gpio(E,0)
	set_gpio(CS,1)

def read_lcm(page,line):
	set_page(page)
	output = 0x00
	for i in range(line):
		output = 0x00
		set_gpio(E,0)
		set_gpio(A0,A0_DATA)
		set_gpio(RW,1)
		set_gpio(CS,0)
		set_gpio(E,1)
		mask=128
		for pin in DATA:
			pin.direction = "in"
			if pin.read():
				output += mask
			mask=int(mask/2)
		set_gpio(E,0)
		set_gpio(CS,1)
	print(hex(output))

def read_lcm_img():
	outimg = [0] * 8192
	for page in range(8):
		set_page(page)
		for line in range(128):
			set_gpio(E,0)
			set_gpio(A0,A0_DATA)
			set_gpio(RW,1)
			set_gpio(CS,0)
			set_gpio(E,1)
			outimg[(page*8*128)+(0*128)+line] = read_gpio(D0)
			outimg[(page*8*128)+(1*128)+line] = read_gpio(D1)
			outimg[(page*8*128)+(2*128)+line] = read_gpio(D2)
			outimg[(page*8*128)+(3*128)+line] = read_gpio(D3)
			outimg[(page*8*128)+(4*128)+line] = read_gpio(D4)
			outimg[(page*8*128)+(5*128)+line] = read_gpio(D5)
			outimg[(page*8*128)+(6*128)+line] = read_gpio(D6)
			outimg[(page*8*128)+(7*128)+line] = read_gpio(D7)
			set_gpio(E,0)
			set_gpio(CS,1)

	for y in range(64):
		for x in range(128):
			print(outimg[(y*128)+x],end="")
		print("")

def init_lcm():
	set_gpio(RS,1)

	for x in [0xae,0xa2,0xa0,0xc8,0xa6,0x40,0x22,0x81,0x3f,0xf8,0x00,0xa4,0x2c]:
		write_lcm(A0_CMD,x)

	write_lcm(A0_CMD,0x2e)
	write_lcm(A0_CMD,0x2f)
	write_lcm(A0_CMD,0xaf);

def exit_lcm():
	RS.close()
	CS.close()
	RW.close()
	A0.close()
	E.close()
	for x in DATA:
		x.close()

def set_page(page):
	write_lcm(A0_CMD,(0xB0 + page))
	write_lcm(A0_CMD,0x10)
	write_lcm(A0_CMD,0x00)

def draw_lcm(image):
	write_lcm(A0_CMD,0xae)
	for page in range(8):
		set_page(page)
		for line in range(128):
			write_lcm(A0_DATA, image[(page*128)+line])
	write_lcm(A0_CMD,0xaf)

def draw_file(path):
	img = [0x00] * 1024
	im = Image.open(path)
	pixels = im.load()

	width  = im.size[0]
	height = im.size[1]

	if width > 128:
		width = 128
	if height > 64:
		height = 64
	for y in range(int(height/8)):
		for x in range(width):
			outbyte = 0x00
			for bit in range(8):
				if pixels[x,(y*8)+bit] != 0:
					outbyte += 2**bit
			img[x+(128*y)] = outbyte
	draw_lcm(img)

init_lcm()
draw_file("example.bmp")
read_lcm_img()
exit_lcm()
