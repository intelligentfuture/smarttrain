#include <ESP8266WiFi.h>
#include "NTPClient.h"
#include <WiFiUDP.h>
#include <Ticker.h>
#include <stdio.h>
#include <string.h>

const char* ssid     = "CTRL_CENT_GW_NODE"; //CTRL_CENT_GW_NODE
const char* password = "ACDINN--"; //ACDINN--
uint16_t chip_id = ESP.getChipId();

IPAddress gw(10, 20, 18, 1);
const int port = 55555;

WiFiUDP ntpUDP;
//NTPClient(UDP& udp, const char* poolServerName, int timeOffset, int updateInterval)
NTPClient timeClient(ntpUDP, "10.20.18.1", 25200, 60000);

WiFiUDP client_obj;

uint8_t sensor_pin[6] = {5, 4, 14, 12, 13, 10}; //[D1 D2 D5 D6 D7, SD3]
uint8_t pin_count = 6;

WiFiEventHandler gotIpEventHandler;
WiFiEventHandler disconnectedEventHandler;

Ticker t1, t2, t3, t4, t5, t6;

unsigned int t_cut[6];
bool state[6] = {0, 0, 0, 0, 0, 0};

bool clientState = false;

uint8_t sendPacket(char data[]){
  uint8_t PACKET_SIZE = strlen(data);
  client_obj.beginPacket(gw, port);
  client_obj.write(data, PACKET_SIZE);
  client_obj.endPacket();
  return PACKET_SIZE;
}

void checkConnection(){
  if(WiFi.status() == WL_CONNECTED){
    if (!clientState){
      Serial.print("Connecting to gateway... ");
      timeClient.update();
      Serial.println("Done!");
      pushData(0xF, 0xF, 0xFFFFFFFF);
      clientState = true;
    }
  }else if(WiFi.status() == WL_DISCONNECTED){
    clientState = false;
  }
}

uint8_t checkReply(char *chk, char *opt){
  if(WiFi.status() == WL_CONNECTED){
    delay(50);
    const uint8_t cb = client_obj.parsePacket();
    if (cb){
      char packetBuffer[255];
      client_obj.read(packetBuffer, cb);
      packetBuffer[cb] = '\0';
      if (strncmp(packetBuffer, chk, cb-1) == 0)
        return 1;
      else if (strncmp(packetBuffer, opt, cb-1) == 0)
        return 2;
    }
   return 0;
  }
}

void count_t(uint8_t idx){
  t_cut[idx]++;
}
unsigned int get_t(uint8_t idx){
  return t_cut[idx];
}
void reset_t(uint8_t idx){
  t_cut[idx] = 0;
}

uint16_t checksum_calc(int data){
  uint16_t tmp = 0;
  tmp += data;
  return (65535-tmp);
}

void pushData(uint8_t sensor_id, uint8_t header_id, unsigned int data){
  unsigned long now = timeClient.getEpochTime();
  uint16_t checksum = checksum_calc(now+chip_id+sensor_id+header_id+data);
  
  char updateTXT[28];
  sprintf(updateTXT, ":%08X%04X%01X%01X%08X%04X\n",now ,chip_id, sensor_id, header_id, data, checksum );
  uint8_t sb = sendPacket(updateTXT);
  Serial.printf("%d Byte >> %s", sb, updateTXT);
}

void handleRISING(uint8_t idx){
  // set tick every 1 ms
  if (!state[idx]){
    switch (idx) {
      case 0:
        t1.attach(0.001, count_t, idx);
        break;
      case 1:
        t2.attach(0.001, count_t, idx);
        break;
      case 2:
        t3.attach(0.001, count_t, idx);
        break;
      case 3:
        t4.attach(0.001, count_t, idx);
        break;
      case 4:
        t5.attach(0.001, count_t, idx);
        break;
      case 5:
        t6.attach(0.001, count_t, idx);
        break;
    }
    state[idx] = 1;
    if (clientState){
        pushData(idx, 0, 0);
    }
  }
}

void handleFALLING(uint8_t idx){
  if (state[idx]){
    if (get_t(idx) > 200){  // minimum time in ms
      switch (idx) {
        case 0:
          t1.detach();
          break;
        case 1:
          t2.detach();
          break;
        case 2:
          t3.detach();
          break;
        case 3:
          t4.detach();
          break;
        case 4:
          t5.detach();
          break;
        case 5:
          t6.detach();
          break;
      }
      if (clientState){
        pushData(idx, 1, get_t(idx));
      }
      reset_t(idx);
      state[idx] = 0;
    }
  }
}

void delay_intl(uint8_t ms){
  uint16_t st = millis();
  uint16_t sp = st+ms;
}

void handleInt0(){
    delay_intl(10);
    if (digitalRead(sensor_pin[0])){
        handleRISING(0);
    }else {
        handleFALLING(0);
    }
}

void handleInt1(){
    delay_intl(10);
    if (digitalRead(sensor_pin[1])){
        handleRISING(1);
    }else {
        handleFALLING(1);
    }
}

void handleInt2(){
    delay_intl(10);
    if (digitalRead(sensor_pin[2])){
        handleRISING(2);
    }else {
        handleFALLING(2);
    }
}

void handleInt3(){
    delay_intl(10);
    if (digitalRead(sensor_pin[3])){
        handleRISING(3);
    }else {
        handleFALLING(3);
    }
}

void handleInt4(){
    delay_intl(10);
    if (digitalRead(sensor_pin[4])){
        handleRISING(4);
    }else {
        handleFALLING(4);
    }
}

void handleInt5(){
    delay_intl(10);
    if (digitalRead(sensor_pin[5])){
        handleRISING(5);
    }else {
        handleFALLING(5);
    }
}

void onGotIP(const WiFiEventStationModeGotIP& evt){
  Serial.print("WiFi Connected, IP: ");
  Serial.println(WiFi.localIP());
}

void onDisconnected(const WiFiEventStationModeDisconnected& evt){
  Serial.println("Wifi disconnected");
}

void setup()
{
  Serial.begin(115200);
  for(int i=0; i<pin_count;i++){
    pinMode(sensor_pin[i], INPUT_PULLUP);
    reset_t(i);
  }
  pinMode(2, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(sensor_pin[0]), handleInt0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[1]), handleInt1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[2]), handleInt2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[3]), handleInt3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[4]), handleInt4, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[5]), handleInt5, CHANGE);

  WiFi.mode(WIFI_STA);
  
  gotIpEventHandler = WiFi.onStationModeGotIP(&onGotIP);
  disconnectedEventHandler = WiFi.onStationModeDisconnected(&onDisconnected);
  
  WiFi.begin(ssid, password);
  WiFi.hostname(String(chip_id).c_str());
  Serial.println();
  Serial.println();
  Serial.printf("ID: %04X, Connect to SSID: %s \n", chip_id, ssid);
  client_obj.begin(port);
  timeClient.begin();
}

void loop() {
  checkConnection();
  digitalWrite(2, 0);
  delay(500);
  digitalWrite(2, 1);
  delay(1000);
}
