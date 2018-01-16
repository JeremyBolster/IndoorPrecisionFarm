#include "DHT22.h" 
DHT dht(DHTPIN, DHTTYPE);
void setup_air_temperature() {
  dht.begin();
}
void setup_humidity() {
  dht.begin();
}

float get_air_temperature() {
  /* This function can return NaN */
  return dht.readTemperature();
}

float get_humidity() {
  /* This function can return NaN */
  return dht.readHumidity();
}
