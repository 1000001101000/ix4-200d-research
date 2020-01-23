#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/gpio.h>
#include <linux/delay.h>
#include <linux/moduleparam.h>
#include <linux/uaccess.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/mutex.h>

#include <linux/string.h>
#include <asm/string.h>

#include "img.h"
#include "font.h"
#include "initImg.h"

/* pin definition */
#define LCM_BUS_RS                      15      //MPP15 use for RS
#define LCM_BUS_A0                      34      //MPP34 use for A0
#define LCM_BUS_CS                      35      //MPP35 use for CS
#define LCM_BUS_RW              44      //MPP44 use for R/W
#define LCM_BUS_E               45      //MPP45 use for E
#define LCM_DATA_BITS           8

// Data pin mapping
//                                 D0  D1  D2  D3  D4  D5  D6  D7
//--------------------------------------------------------------
static int data_pin_mapping[8] = { 36, 37, 38, 39, 40, 41, 42, 43 };

#define FIRST_PIN 34
#define LAST_PIN 45

#define NBLINES 128
#define NBPAGES	8

#define A0_DAT                          0x01
#define A0_CMD                          0x00
#define PIN_IN                          0x01
#define PIN_OUT                         0x00
#define RS_WRITE                        0x00
#define RS_READ                         0x01

#define INIT_PACKAGE_SIZE 13
unsigned char  initial_lcm_pkg[INIT_PACKAGE_SIZE]=
{
		0xae,   //1
                0xa2,   //2
                0xa0,   //3
                0xc8,   //4
                0xa6,   //5
                0x40,   //6     //0x41
                0x22,   //7
                0x81,   //8
                0x3f,   //9
                0xf8,   //10
                0x00,   //11
                0xa4,   //12
                0x2c,   //13
};


void write_lcm(int A0type,unsigned char tmp)
{
        u32 i=0;

        //set data our TODO: already done by init but to be checked

        //pin E down
        gpio_set_value(LCM_BUS_E, 0x0);

        for ( i=0; i<LCM_DATA_BITS; i++)
        {
                gpio_set_value( data_pin_mapping[i], (tmp&0x01) );
                tmp = tmp >> 1;
        }

        //prepare A0
        gpio_set_value( LCM_BUS_A0, (A0type & 0x01) );
        udelay(30);
        //prepare RW
        gpio_set_value( LCM_BUS_RW, 0x0 );
        gpio_set_value( LCM_BUS_CS, 0x0 );
        //pin E up
        gpio_set_value(LCM_BUS_E, 0x1);
        udelay(100);
        //pin E down
        gpio_set_value(LCM_BUS_E, 0x0);
        gpio_set_value( LCM_BUS_CS, 0x1 );
        udelay(100);

        return;
}

void initialize_lcm(void)
{
        for (i = 0; i< INIT_PACKAGE_SIZE; i++)
                write_lcm(A0_CMD,initial_lcm_pkg[i]);

        mdelay(200);//delay 200ms
        write_lcm(A0_CMD,0x2e);
        mdelay(200);//delay 200ms
        write_lcm(A0_CMD,0x2f);
        mdelay(400);//delay 400ms
        write_lcm(A0_CMD,0xaf);
}

static void clear_lcm(void)
{
        u8 page = 0;
        u8      dat = 0;
        
        write_lcm(A0_CMD,0xae); //display off
         for(page =0 ;page<NBPAGES;page++)
         {
                write_lcm(A0_CMD, page|0xb0);
                write_lcm(A0_CMD, ( (0x0>>4)&0x0f)|0x10 );
                write_lcm(A0_CMD,  (0x0&0x0f) );
                for(dat=0;dat<NBLINES;dat++)
                {
                        write_lcm(A0_DAT, 0 );        
                }        
         }
         write_lcm(A0_CMD,0xaf); //display on    
}

static void draw_lcm(void)
{
        u8 page = 0;
        u8      dat = 0;

        write_lcm(A0_CMD,0xae); //display off
         for(page =0 ;page<NBPAGES;page++)
         {
                write_lcm(A0_CMD, page|0xb0);
                write_lcm(A0_CMD, ( (0x0>>4)&0x0f)|0x10 );
                write_lcm(A0_CMD,  (0x0&0x0f) );
                for(dat=0;dat<NBLINES;dat++)
                {
                        write_lcm(A0_DAT, img[page*NBLINES+dat] );
                }
         }
         write_lcm(A0_CMD,0xaf); //display on
}


static void draw_init(void)
{
	memcpy(img, initImg, sizeof(img));
        draw_lcm();
}

static void wixlcm_close(void)
{
	u32 i=0;

        for (i=FIRST_PIN; i<=LAST_PIN; i++) {
	        // turn LED off
	        gpio_set_value(i, 0);

	        // unregister GPIO
	        gpio_free(i);
        }
}
0;
}

int main()
{
        int ret = 0;
		u32 i=0;
        char name[5];

        for (i=FIRST_PIN; i<=LAST_PIN; i++) {
        	sprintf(name, "lcm%d", i);
        	// register, turn off
        	ret = gpio_request_one(i, GPIOF_OUT_INIT_LOW, name);
        }

        //E is already down but should be if init doesn't

        //RS up
        gpio_set_value(LCM_BUS_RS, 0x1);

	initialize_lcm();
	clear_lcm();
    draw_init();
	wixlcm_close();
	return ret;
}

