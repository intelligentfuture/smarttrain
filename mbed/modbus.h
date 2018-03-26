#ifndef MODBUS_H
#define MODBUS_H

#define FUNC_CODE       3
#define ADDR_BASE       0x0000
#define ADDR_RANGE      2
#define MAX_FRAME_SIZE  20

void modbus_init(uint8_t id);
uint16_t modbus_read(uint16_t offset);
uint16_t modbus_update(uint8_t offset, uint16_t val);
int modbus_parser(char ch, uint8_t *frame);
uint8_t modbus_check(uint16_t offset, uint16_t count);
void modbus_response(uint8_t reg_map, char *rttmp);

#endif // MODBUS_H
