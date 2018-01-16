// DS18b20.h
#ifndef DS18b20_H
#define DS18b20_H

#include "OneWire.h"
const int WATER_TEMP_PIN = 10;
void setup_water_temperature();
float get_water_temperature();

#endif
