#include "MH_Z14A.h"

float get_co2(){
  float volts = analogRead(A8) * 5.0 / (float) 1024;
  float CO2_val = (volts - 0.4) * (float) 5000 / 1.6;
	return CO2_val;
}

void setup_co2(){
	pinMode(CO2_PIN, INPUT);
}
