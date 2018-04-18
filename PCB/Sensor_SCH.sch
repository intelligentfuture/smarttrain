EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Sensor_SCH-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L LM393 U1
U 1 1 5ABB1783
P 6650 3100
F 0 "U1" H 6800 3250 50  0000 C CNN
F 1 "LM393" H 6900 2950 50  0000 C CNN
F 2 "" H 6650 3100 50  0001 C CNN
F 3 "" H 6650 3100 50  0001 C CNN
	1    6650 3100
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x03 J1
U 1 1 5ABB17FD
P 6850 2150
F 0 "J1" H 6850 2350 50  0000 C CNN
F 1 "Conn_01x03" H 6850 1950 50  0000 C CNN
F 2 "" H 6850 2150 50  0001 C CNN
F 3 "" H 6850 2150 50  0001 C CNN
	1    6850 2150
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5ABB1834
P 4200 2950
F 0 "R1" V 4280 2950 50  0000 C CNN
F 1 "R" V 4200 2950 50  0000 C CNN
F 2 "" V 4130 2950 50  0001 C CNN
F 3 "R" H 4200 2950 50  0001 C CNN
	1    4200 2950
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 5ABB1871
P 5200 2700
F 0 "R3" V 5280 2700 50  0000 C CNN
F 1 "R" V 5200 2700 50  0000 C CNN
F 2 "" V 5130 2700 50  0001 C CNN
F 3 "" H 5200 2700 50  0001 C CNN
	1    5200 2700
	1    0    0    -1  
$EndComp
Text Label 6300 2050 0    60   ~ 0
Data
Text Label 6300 2150 0    60   ~ 0
Vcc
Text Label 6300 2250 0    60   ~ 0
GND
Text Label 6950 3100 0    60   ~ 0
Data
Text Label 6550 2800 1    60   ~ 0
Vcc
Wire Wire Line
	6650 2050 6300 2050
Wire Wire Line
	6650 2150 6300 2150
Wire Wire Line
	6650 2250 6300 2250
Text Label 6550 3400 3    60   ~ 0
GND
Text Label 4200 2800 1    60   ~ 0
Vcc
Text Label 5200 2550 1    60   ~ 0
Vcc
$Comp
L LED D1
U 1 1 5ABB1A2C
P 4200 3250
F 0 "D1" H 4200 3350 50  0000 C CNN
F 1 "LED" H 4200 3150 50  0000 C CNN
F 2 "" H 4200 3250 50  0001 C CNN
F 3 "" H 4200 3250 50  0001 C CNN
	1    4200 3250
	0    -1   -1   0   
$EndComp
Text Label 4200 3400 3    60   ~ 0
GND
$Comp
L LDR07 R4
U 1 1 5ABB1BCF
P 5200 3250
F 0 "R4" V 5000 3250 50  0000 C CNN
F 1 "LDR07" V 5275 3250 50  0000 C TNN
F 2 "" V 5375 3250 50  0001 C CNN
F 3 "" H 5200 3200 50  0001 C CNN
	1    5200 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 2850 5200 3100
Text Label 5200 3400 3    60   ~ 0
GND
$Comp
L POT RV1
U 1 1 5ABB1C41
P 5800 3200
F 0 "RV1" V 5625 3200 50  0000 C CNN
F 1 "POT" V 5700 3200 50  0000 C CNN
F 2 "" H 5800 3200 50  0001 C CNN
F 3 "" H 5800 3200 50  0001 C CNN
	1    5800 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5800 3050 5800 2550
Wire Wire Line
	5800 3350 5800 3400
Text Label 5800 2550 1    60   ~ 0
Vcc
Text Label 5800 3400 3    60   ~ 0
GND
Wire Wire Line
	6350 3200 5950 3200
Wire Wire Line
	6350 3000 5200 3000
Connection ~ 5200 3000
$Comp
L R R2
U 1 1 5ABB8159
P 4700 3250
F 0 "R2" V 4780 3250 50  0000 C CNN
F 1 "R" V 4700 3250 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 3250 50  0001 C CNN
F 3 "" H 4700 3250 50  0001 C CNN
	1    4700 3250
	1    0    0    -1  
$EndComp
Text Label 4700 2800 1    60   ~ 0
Data
$Comp
L LED D2
U 1 1 5ABB8160
P 4700 2950
F 0 "D2" H 4700 3050 50  0000 C CNN
F 1 "LED" H 4700 2850 50  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 4700 2950 50  0001 C CNN
F 3 "" H 4700 2950 50  0001 C CNN
	1    4700 2950
	0    -1   -1   0   
$EndComp
Text Label 4700 3400 3    60   ~ 0
GND
$EndSCHEMATC
