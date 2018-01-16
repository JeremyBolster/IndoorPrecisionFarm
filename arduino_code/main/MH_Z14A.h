// MH-Z14A.h
#ifndef MH_Z14A_H
#define MH_Z14A_H
#include <Arduino.h>

#define CO2_PIN 	A1 // The pin that the CO2 sensor is connected to (Analog)
// datasheet: https://www.openhacks.com/uploadsproductos/mh-z14_co2.pdf

void setup_co2();
float get_co2();

#endif
