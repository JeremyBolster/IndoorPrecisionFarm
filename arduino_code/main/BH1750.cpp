#include "BH1750.h"


BH1750 lightMeter;

void setup_lux(){

  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();
  lightMeter.begin();

}

float get_lux() {
  float lux = (float) lightMeter.readLightLevel();
  return lux;
}