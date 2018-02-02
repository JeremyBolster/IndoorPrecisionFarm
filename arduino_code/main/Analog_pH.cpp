#include "Analog_pH.h"


void setup_pH(){}

float get_pH() {
  float voltage = analogRead(pH_PIN)*5.0/1024;
  float pHValue = 3.5*voltage+Offset;
  return pHValue;
}