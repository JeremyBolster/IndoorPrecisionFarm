// dht22.h
#ifndef DHT22_H
#define DHT22_H
#include "DHT.h"

#define DHTPIN            2         // Pin which is connected to the DHT sensor.
#define DHTTYPE           DHT22     // DHT 22 (AM2302)

// See guide for details on sensor wiring and usage:
//   https://learn.adafruit.com/dht/overview

void setup_air_temperature();
void setup_humidity();
float get_air_temperature();
float get_humidity();

#endif
