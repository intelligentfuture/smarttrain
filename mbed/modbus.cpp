#include "mbed.h"
#include "modbus.h"

uint8_t nodeId = 0;
uint16_t regValue[ADDR_RANGE];

enum state {IDLE, RECEPTION, END} protState = IDLE;

int process_buffer(char *buf, uint8_t *frame)
{
    int status = 0;
    uint8_t sum = 0;
    uint8_t lrc, i;
    char tmpbuf[] = {0, 0, 0};
    
    if (strlen(buf) == 14) {
        for (i = 0; i < 6; i++) {
            tmpbuf[0] = buf[i*2];
            tmpbuf[1] = buf[i*2 + 1]; 
            frame[i] = strtoul(tmpbuf, NULL, 16);
        }
        tmpbuf[0] = buf[12]; tmpbuf[1] = buf[13]; 
        lrc = strtoul(tmpbuf, NULL, 16);
        for (i = 0; i < 6; i++) {
            sum += frame[i];
        }
        sum = sum + lrc;
        if (sum == 0) {
            status = 1;
        }
    }
    
    return status;    
}

void modbus_init(uint8_t id)
{
    int i;
    
    nodeId = id;
    for (i = 0; i < ADDR_RANGE; i++) {
        regValue[i] = 0;
    }
}

uint16_t modbus_read(uint16_t offset)
{  
    if (offset < ADDR_RANGE) {
        uint16_t tmp = regValue[offset];
        modbus_update(offset, 0x0000);
        return tmp;
        
    } 
    return 0;
}

uint16_t modbus_update(uint8_t offset, uint16_t val)
{
    uint16_t tmp;
    
    if (offset < ADDR_RANGE) {
        tmp = regValue[offset];
        regValue[offset] = val;
        return tmp;
    } 
    return 0;
}

uint8_t modbus_check(uint16_t offset, uint16_t count) 
{
    uint8_t reg_map = 0x00;
    int i, j;
    
    for (i = 0; i < ADDR_RANGE; i++) {
        for (j = offset; j < (offset+count); j++) {
            if (j == (ADDR_BASE + i)) {
                reg_map |= (1 << i);
            } 
        }
    }
    
    return reg_map;
}

int modbus_parser(char ch, uint8_t *frame)
{
    static char buf[514];
    static int idx = 0;
    static int status = 0;
    
    switch(protState) {
        case IDLE:
            if (ch == ':') {
                protState = RECEPTION;
                idx = 0;
                status = 0;
            }
            break;
        case RECEPTION:
            //printf("%c", ch);
            if ((ch >= '0') && (ch <= '9')) {
                buf[idx++] = ch;
            } else if ((ch >= 'a') && (ch <= 'f')) {
                buf[idx++] = ch;
            } else if ((ch >= 'A') && (ch <= 'F')) {
                buf[idx++] = ch;
            } else if (ch == '\r' and idx > 4) {
                buf[idx] = 0;
                protState = END;
            } else {
                protState = IDLE;
            }
            break;
        case END:
            if (ch == '\n') {
                if (process_buffer(buf, frame)) {
                    if ((frame[0] == nodeId) && (frame[1] == FUNC_CODE)) {
                        status = 1;
                    }
                }
            } 
            protState = IDLE;
            break;
        default:
            protState = IDLE;
    }
    
    return status;
}

uint8_t calc_lrc(uint8_t *frame, int count)
{
    int8_t lrc = 0;
    int i;
    
    for (i = 0; i < count; i++) {
        lrc += frame[i];
    }
    return -lrc;
}

void modbus_response(uint8_t reg_map, char *rttmp) 
{
    char fmt00[] = ":%02X%02X%02X\r\n";
    char fmt01[] = ":%02X%02X%02X%02X%02X\r\n";
    char fmt02[] = ":%02X%02X%02X%02X%02X\r\n";
    char fmt03[] = ":%02X%02X%02X%02X%02X%02X%02X\r\n";
    char *fmtstr;
    uint8_t frame[ADDR_RANGE*2 + 3];
    uint16_t tmp;
    
    frame[0] = nodeId;
    frame[1] = FUNC_CODE;
    switch(reg_map) {
        case 1:
            tmp = modbus_read(0);
            frame[2] = tmp >> 8;
            frame[3] = tmp & 0xFF;
            frame[4] = calc_lrc(frame, 4);
            fmtstr = fmt01;
            sprintf(rttmp, fmtstr, frame[0], frame[1], frame[2], frame[3], frame[4]);
            //printf("Response: %s", str);
            //printf(str);
            break;
        case 2:
            tmp = modbus_read(1);
            frame[2] = tmp >> 8;
            frame[3] = tmp & 0xFF;
            frame[4] = calc_lrc(frame, 4);
            fmtstr = fmt02;
            sprintf(rttmp, fmtstr, frame[0], frame[1], frame[2], frame[3], frame[4]);
            //printf("Response: %s", str);     
            //printf(str);   
            break;
        case 3:
            tmp = modbus_read(0);
            frame[2] = tmp >> 8;
            frame[3] = tmp & 0xFF;
            tmp = modbus_read(1);
            frame[4] = tmp >> 8;
            frame[5] = tmp & 0xFF;                                
            frame[6] = calc_lrc(frame, 6);
            fmtstr = fmt03;
            sprintf(rttmp, fmtstr, frame[0], frame[1], frame[2], frame[3], frame[4], frame[5], frame[6]);
            //printf("Response: %s", str);     
            //printf(str);         
            break;
        default:
            fmtstr = fmt00;
            frame[2] = calc_lrc(frame, 2);
            sprintf(rttmp, fmtstr, frame[0], frame[1], frame[2]);
            //printf("Response: %s", str);      
    }
}
