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
const uint8_t pin_count = 6;

WiFiUDP ntpUDP;
//NTPClient(UDP& udp, const char* poolServerName, int timeOffset, int updateInterval)
NTPClient timeClient(ntpUDP, "10.20.18.1", 25200, 60);

WiFiUDP client_obj;

uint8_t sensor_pin[pin_count] = {13, 12, 14, 4, 5, 10}; //[D7 D6 D5 D2 D1, SD3]


WiFiEventHandler gotIpEventHandler;

Ticker t1, t2, t3, t4, t5, t6;
Ticker p0, p1, p2, p3, p4, p5;

unsigned int t_cut[pin_count];
bool state[pin_count] = {0, 0, 0, 0, 0, 0};

bool clientState = false;
bool ntpState = false;

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
      Serial.println("Done!");
      if (!ntpState){
        timeClient.update();
        Serial.print("System time: ");
        Serial.println(timeClient.getFormattedTime());
        if (timeClient.getEpochTime()> 252000){
          ntpState = true;
        }
      }
      clientState = true;
      pushData(0xF, 0xF, 0xFFFFFFFF);
    }
  }else{
    clientState = false;
  }
  digitalWrite(2, clientState);
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
  if(clientState){
    digitalWrite(2, 0);
    unsigned long now = timeClient.getEpochTime();
    uint16_t checksum = checksum_calc(now+chip_id+sensor_id+header_id+data);
    
    char updateTXT[28];
    sprintf(updateTXT, ":%08X%04X%01X%01X%08X%04X\n",now ,chip_id, sensor_id, header_id, data, checksum );
    uint8_t sb = sendPacket(updateTXT);
    Serial.printf("%d Byte >> %s", sb, updateTXT);
    digitalWrite(2, 1);
  }
}

void handleRISING(uint8_t idx){
  // set tick every 1 ms
  
  Serial.printf("R%d ", idx);
  if (!state[idx]){
    switch (idx) {
      case 0:
        t1.attach_ms(1, count_t, idx);
        break;
      case 1:
        t2.attach_ms(1, count_t, idx);
        break;
      case 2:
        t3.attach_ms(1, count_t, idx);
        break;
      case 3:
        t4.attach_ms(1, count_t, idx);
        break;
      case 4:
        t5.attach_ms(1, count_t, idx);
        break;
      case 5:
        t6.attach_ms(1, count_t, idx);
        break;
    }
    pushData(idx, 0, 0);
    state[idx] = 1;
  }
}

void handleFALLING(uint8_t idx){
  Serial.printf("F%d ", idx);
  if (state[idx]){
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
    pushData(idx, 1, get_t(idx));
    reset_t(idx);
    state[idx] = 0;
  }
}

void handleInterupt(int pin){
    if (digitalRead(sensor_pin[pin])){
        handleRISING(pin);
    }else {
        handleFALLING(pin);
    }
}

void debounce_p0(){
  p0.once_ms(100, handleInterupt, 0);
}
void debounce_p1(){
  p1.once_ms(100, handleInterupt, 1);
}
void debounce_p2(){
  p2.once_ms(100, handleInterupt, 2);
}
void debounce_p3(){
  p3.once_ms(100, handleInterupt, 3);
}
void debounce_p4(){
  p4.once_ms(100, handleInterupt, 4);
}
void debounce_p5(){
  p5.once_ms(100, handleInterupt, 5);
}

void onGotIP(const WiFiEventStationModeGotIP& evt){
  Serial.print("WiFi Connected, IP: ");
  Serial.println(WiFi.localIP());
}

void setup()
{
  ESP.eraseConfig();
  pinMode(2, OUTPUT);
  digitalWrite(2, 0);
  Serial.begin(115200);
  for(int i=0; i<pin_count;i++){
    pinMode(sensor_pin[i], INPUT_PULLUP);
    reset_t(i);
  }
  
  gotIpEventHandler = WiFi.onStationModeGotIP(&onGotIP);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true);
  WiFi.begin(ssid, password);
  WiFi.hostname(String(chip_id, HEX));
  Serial.println();
  Serial.println();
  Serial.printf("ID: %04X, Connect to SSID: %s \n", chip_id, ssid);
  
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
  }
  
  client_obj.begin(port);
  timeClient.begin();
  
  attachInterrupt(digitalPinToInterrupt(sensor_pin[0]), debounce_p0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[1]), debounce_p1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[2]), debounce_p2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[3]), debounce_p3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[4]), debounce_p4, CHANGE);
  attachInterrupt(digitalPinToInterrupt(sensor_pin[5]), debounce_p5, CHANGE);
}

void loop() {
  checkConnection();
  delay(5000);
}
