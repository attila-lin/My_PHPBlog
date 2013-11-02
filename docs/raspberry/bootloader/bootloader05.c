//-------------------------------------------------------------------------
//-------------------------------------------------------------------------

// The raspberry pi firmware at the time this was written defaults
// loading at address 0x8000.  Although this bootloader could easily
// load at 0x0000, it loads at 0x8000 so that the same binaries built
// for the SD card work with this bootloader.  Change the ARMBASE
// below to use a different location.

#define ARMBASE 0x8000

#define LOAD    0x00
#define GO      0x01
#define PEEK    0x02
#define POKE    0x03
#define VERIFY  0x04

extern void PUT32 ( unsigned int, unsigned int );
extern void PUT16 ( unsigned int, unsigned int );
extern void PUT8 ( unsigned int, unsigned int );
extern unsigned int GET32 ( unsigned int );
extern unsigned int GET8 ( unsigned int );
extern unsigned int GETPC ( void );
extern void BRANCHTO ( unsigned int );
extern void dummy ( unsigned int );

extern void uart_init ( void );
extern unsigned int uart_lcr ( void );
extern void uart_flush ( void );
extern void uart_send ( unsigned int );
extern unsigned int uart_recv ( void );
extern void hexstring ( unsigned int );
extern void hexstrings ( unsigned int );
extern void timer_init ( void );
extern unsigned int timer_tick ( void );

extern void timer_init ( void );
extern unsigned int timer_tick ( void );

void puts(char* s);

//------------------------------------------------------------------------
unsigned char xstring[256];
//------------------------------------------------------------------------
int notmain ( void ) {
    unsigned int ra;
    //unsigned int rb;
    unsigned int rx;
    unsigned int addr;
    unsigned int block;
    unsigned int state;

    unsigned int crc;

    unsigned int error_addr;

    uart_init();
    hexstring(0x12345678);
    hexstring(GETPC());
    hexstring(ARMBASE);
    puts("Hello World!");
    uart_send(0x04);
    timer_init();

//SOH 0x01
//ACK 0x06
//NAK 0x15
//EOT 0x04

//block numbers start with 1

//132 byte packet
//starts with SOH
//block number byte
//255-block number
//128 bytes of data
//checksum byte (whole packet)
//a single EOT instead of SOH when done, send an ACK on it too
    addr=ARMBASE;
    error_addr = 0;
    block=1;
    state=0;
    crc=0;
    rx=timer_tick();

    while(1) {
        ra=timer_tick();
        if((ra-rx)>=4000000) {
            uart_send(0x15);
            rx+=4000000;
        }

        if((uart_lcr()&0x01)==0) continue;

        xstring[state]=uart_recv();
        rx=timer_tick();

        switch(state) {
            case 0: {
                if(xstring[state]==0x01) {
                    crc=xstring[state];
                    state++;
                }
                else if (xstring[state] == 0x04) {
                    uart_send(0x06);
                    if (xstring[1] == LOAD) {
                        puts("LOADED");
                        uart_send(0x04);
                        uart_flush();
                    }
                    else if (xstring[1] == VERIFY) {
                        if (error_addr == 0) {
                            puts("VERIFY SUCCESS");
                            uart_send(0x04);
                        }
                        else {
                            puts("VERIFY ERROR");
                            puts("MEM ADDRESS:");
                            hexstring(error_addr);
                            puts("MEM VALUE:");
                            hexstring(GET32(error_addr));
                            uart_send(0x04);
                        }
                        uart_flush();
                    }
                    addr = ARMBASE;
                    error_addr = 0;
                    block = 1;
                    state = 0;
                    crc = 0;
                }
                else {
                    state=0;
                    uart_send(0x15);
                    puts("INITIAL ERROR");
                    uart_send(0x04);
                    uart_flush();
                }
                break;
            }
            case 1: {
                if (xstring[1] > VERIFY) {
                    state = 0;
                    uart_send(0x15);
                    puts("INVALID COMMAND");
                    uart_send(0x04);
                    uart_flush();
                }
                else if (xstring[1] == GO) {
                    state = 0;
                    uart_send(0x06);
                    puts("GO TO TARGET");
                    uart_send(0x04);
                    uart_flush();
                    BRANCHTO(ARMBASE);
                }
                else if (xstring[1] == PEEK || xstring[1] == POKE) {
                    state = 133;
                }
                else {
                    state++;
                }
                break;
            }
            case 2: {
                if(xstring[state]==block) {
                    crc+=xstring[state];
                    state++;
                }
                else {
                    state=0;
                    uart_send(0x15);
                    puts("BLOCK ERROR");
                    uart_send(0x04);
                    uart_flush();
                }
                break;
            }
            case 3: {
                if(xstring[state]==(0xFF-xstring[state-1])) {
                    crc+=xstring[state];
                    state++;
                }
                else {
                    state=0;
                    uart_send(0x15);
                    puts("BLOCK ERROR");
                    uart_send(0x04);
                    uart_flush();
                }
                break;
            }
            case 132: {
                crc&=0xFF;
                if(xstring[state]==crc) {
                    if (xstring[1] == LOAD) {
                        for(ra=0;ra<128;ra++) {
                            PUT8(addr++,xstring[ra+4]);
                        }
                        uart_send(0x06);
                    }
                    else {
                        for (ra = 0; ra < 128; ra++, addr++) {
                            if (xstring[ra + 4] != (GET8(addr) & 0xff)) {
                                error_addr = addr;
                                break;
                            }
                        }
                        uart_send(0x06);
                    }
                    block=(block+1) & 0xFF;
                }
                else {
                    uart_send(0x15);
                    puts("CRC ERROR");
                    uart_send(0x04);
                    uart_flush();
                }
                state=0;
                break;
            }
            case 136: {
                if (xstring[1] == PEEK) {
                    unsigned int peek_addr = 0;
                    for (ra = 0; ra < 4; ra++) {
                        peek_addr = peek_addr << 8 | xstring[ra + 133];
                    }
                    uart_send(0x06);
                    puts("PEEK");
                    hexstring(GET32(peek_addr));
                    uart_send(0x04);
                    uart_flush();
                    state = 0;
                }
                else {
                    state++;
                }
                break;
            }
            case 140: {
                if (xstring[1] == POKE) {
                    unsigned int poke_addr = 0x00000000;
                    unsigned int poke_data = 0;
                    for (ra = 0; ra < 4; ra++) {
                        poke_addr = poke_addr << 8 | xstring[ra + 133];
                        poke_data = poke_data << 8 | xstring[ra + 137];
                    }
                    uart_send(0x06);
                    puts("POKE");
                    PUT32(poke_addr, poke_data);
                    uart_send(0x04);
                    uart_flush();
                    state = 0;
                }
                else {
                    state = 0;
                }
                break;
            }
            default: {
                crc+=xstring[state];
                state++;
                break;
            }
        }
    }
    return(0);
}

void puts(char* s) {
    int i = 0;
    while(s[i] != '\0') {
        uart_send(s[i++]);
    }
    uart_send(0x0D);
    uart_send(0x0A);
}

