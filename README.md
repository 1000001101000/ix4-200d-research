ix4-200d-research
========
![alt text](https://github.com/1000001101000/ix4-200d-research/raw/master/.img/CE157618-AECE-4693-A405-F29781FA5CDE.jpeg)

Mainline linux on ix4-200d

Tools for using Debian on the ix4-200d, an extension of the work done by:

https://github.com/benoitm974/ix4-300d/ <br/>
https://forum.doozan.com/read.php?2,22623


Status
========
LCD:

I've modified the kernel driver provided by @benoitm974 for the LCD screen to work with the pin layout for this model and added an initial image which displays when it is loaded. I've also modified the Makefile to allow compiling directly on the device or crosscompile as needed. I've also set up a CI/CD workflow to automatically generate binaries for the kernels commonly used by Debian and place them in the bins/ directory.

The kernel module was originally developed for 3.XX kernels and is pretty unstable for modern kernels. The inital image is displaying succesfully but attempting to send commands to the device seems to trigger a segfault so currently I've just used it for testing. 

Rather than try to fix/improve the kernel driver (I'm not much of a kernel developer) I'll be looking at creating a userland solution using Python/etc. In theory pyLCD should be able to drive it though I haven't had much luck getting it to install on Vanilla Debian.

Device-tree:
I've added entries to the device-tree posted on the Doozan forum to add support for the LEDs and Buttons for this device. I'll be working with them to get them added to their version once I get them finalized. I've also added NAND partitions to properly handle the stock firmware's layout. 

The current version posted here works for kernels 4.19+ (probably somewhat earler as well) but the ethernet does not work with version 4.9. This requires a fairly simple fix which I will probably deal with sometime in the future. 

Other hardware notes:
I've identified 2 additional i2c devices at 0x20 and 0x64, I currently do not know what they are but will add support when/if I figure that out.

The brightness of the LCD and LEDs are controlled by the adt7473 (same as for ix4-300d). It can be set via /sys/class/i2c-adapter/i2c-0/0-002e/pwm3

I suspect the sata led is tied directly to the sata controller but have not been able to verify that, see below.

Installation:
This device works with Debian's "Marvell" kernel but lacks the drivers needed to drive the LEDs. I've added that driver to the custom kernel I maintain for the Terastation III and plan to add it to my custom installer:
https://github.com/1000001101000/Debian_on_Buffalo

I'll add more infor here once I've created those images.

Issues:
The device I'm working with fails to initialize sata. It was listed a broken when I got it so it is possible it simply doesn't work. It does not seem to be specific to the OS/kernel since it also doesn't work in the stock u-boot either. Likewise, the various posts on the Doozan forum seem to show their sata working which further leads me to think it's a problem with my device.

I'm still looking into this issue but it will limit my research somewhat if I can't make it work.



