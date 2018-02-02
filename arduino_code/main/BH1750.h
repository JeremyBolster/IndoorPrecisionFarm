// BH1750.h
#ifndef BH1750_H
#define BH1750_H
#include <Arduino.h>
#include <Wire.h>
#include <BH1750.h>
 	
// library: https://github.com/claws/BH1750

void setup_lux();
float get_lux();

#endif