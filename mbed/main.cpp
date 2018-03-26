#include "mbed.h"
#include "modbus.h"
#include "RawSerial.h"

DigitalOut myled(LED1);
DigitalOut rs485_en(D2);
AnalogIn analog_value(A0);

//RawSerial pc(USBTX, USBRX, 57600);
RawSerial comm(PC_6, PC_7, 57600);

InterruptIn button(USER_BUTTON);
Ticker timebase;

float meas_r;
int state = 0;

uint32_t Tick = 0;
uint32_t pressedTick = 0; 
uint32_t releasedTick = 0;

void serial_callback()
{
    uint8_t frame[6];
    uint16_t offset, count;
    uint8_t reg_map;
    char tmp[20];
    
    char ch = comm.getc();
    if (modbus_parser(ch, frame)) {
        offset = (frame[2] << 8) | (frame[3]);
        count = (frame[4] << 8) | (frame[5]);
        reg_map = modbus_check(offset, count);
        modbus_response(reg_map, tmp);
        rs485_en = 1;
        wait(0.01);
        comm.printf(tmp);
        wait(0.01);
        rs485_en = 0;
    }
}

void pressed_callback()
{
    uint16_t skipCount;
    
    if ((Tick > pressedTick) && (Tick > releasedTick)) {
        skipCount = Tick - releasedTick;
        modbus_update(0x0000, skipCount);
        pressedTick = Tick;
        // printf("Pressed: %d - %d - %d\r\n", pressedTick, releasedTick, skipCount);
    }
}

void released_callback()
{
    uint16_t widthCount;
    
    if ((Tick > pressedTick) && (Tick > releasedTick)) {
        widthCount = Tick - pressedTick;
        modbus_update(0x0001, widthCount);
        releasedTick = Tick;
        // printf("Released: %d - %d - %d\r\n", pressedTick, releasedTick, widthCount);
    }
}

void adc_comparator_with_hysteresis(){
    
    meas_r = analog_value.read();
//    printf("%.3f\n", meas_r);
    if(meas_r > 0.6f){
        if(state == 0){
            state = 1;
//            printf("pressed_callback \n");
            pressed_callback();
            
        }
    }else if(meas_r < 0.4f){
        if(state == 1){
            state = 0;
//            printf("released_callback \n");
            released_callback();   
        }      
    }
}

void ticker_callback()
{
    Tick++;
    adc_comparator_with_hysteresis();
}

int main() {
    rs485_en = 0;
    // setup code
    comm.attach(&serial_callback);
    modbus_init(0x0002); // init ID=02 :020300000002F9
    
    // 1. button code
    button.rise(&pressed_callback);
    button.fall(&released_callback);
    
    // 2. timer code
    timebase.attach(&ticker_callback, 0.1);
//    printf("Starting\n");
//    printf("Test: %02X\r\n", modbus_check(0x0000, 0x0001));
//    printf("Test: %02X\r\n", modbus_check(0x0001, 0x0001));
//    printf("Test: %02X\r\n", modbus_check(0x0000, 0x0002));
//    printf("Test: %02X\r\n", modbus_check(0x0000, 0x0003));
//    printf("Test: %02X\r\n", modbus_check(0x0001, 0x0002));
//    printf("Test: %02X\r\n", modbus_check(0x0002, 0x0002));    
    while(1) {
        // blinking LED
        myled = state;
        wait(0.1);
        //printf("Detection: %d - %d\r\n", pressedTick, releasedTick);
        //modbus_response(0x01);
        //modbus_response(0x02);
        //modbus_response(0x03);
    }
}
