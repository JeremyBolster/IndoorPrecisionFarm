// Analog_pH.h
#ifndef ANALOG_PH_H
#define ANALOG_PH_H
#include <Arduino.h>


#define Offset 0.00
#define pH_PIN A0

void setup_pH();
float get_pH();

#endif