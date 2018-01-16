#include "CmdMessenger.h"
#include "DHT22.h"
#include "DS18b20.h"
#include "BH1750.h"
#include "Analog_pH.h"
#include "MH_Z14A.h"


/* Define available CmdMessenger commands */
enum {
  sensorValue,
  commandReceived,
  toggleDevice,
  poll,
  error
};
/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger cmdMessenger = CmdMessenger(Serial,',',';','/');
/* Create callback functions to deal with incoming messages */
/* callback */
void on_poll(void){
/* We need to loop through all of the sensors to send each of their values in turn */
  String humidity           = String(get_humidity());
  String air_temperature    = String(get_air_temperature());
  String co2_ppm            = String(get_co2());
  String water_temperature  = String(get_water_temperature());
  String lux                = String(get_lux());
  String pH                 = String(get_pH());

  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("humidity");
  cmdMessenger.sendCmdArg(humidity);
  cmdMessenger.sendCmdEnd();
  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("air_temp");
  cmdMessenger.sendCmdArg(air_temperature);
  cmdMessenger.sendCmdEnd();
  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("co2");
  cmdMessenger.sendCmdArg(co2_ppm);
  cmdMessenger.sendCmdEnd();
  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("water_temp");
  cmdMessenger.sendCmdArg(water_temperature);
  cmdMessenger.sendCmdEnd();
  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("lux");
  cmdMessenger.sendCmdArg(lux);
  cmdMessenger.sendCmdEnd();
  cmdMessenger.sendCmdStart(sensorValue);
  cmdMessenger.sendCmdArg("pH");
  cmdMessenger.sendCmdArg(pH);
  cmdMessenger.sendCmdEnd();
}
/* callback */ 
void on_toggle_device(void){
  int devicePin             =  cmdMessenger.readBinArg<int>();
  bool desiredDeviceStatus  =  cmdMessenger.readBinArg<bool>();

  digitalWrite(devicePin, desiredDeviceStatus);
}
/* callback */
void on_unknown_command(void){
    cmdMessenger.sendCmd(error,"Command without callback.");
}
/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
    cmdMessenger.attach(toggleDevice, on_toggle_device);
    cmdMessenger.attach(poll, on_poll);
    cmdMessenger.attach(on_unknown_command);
}

void setup() {
    Serial.begin(BAUD_RATE);
    attach_callbacks();
    
    setup_water_temperature();
    setup_air_temperature();
    setup_co2();
    setup_humidity();
    setup_lux();
    setup_pH();
}

void loop() {
    cmdMessenger.feedinSerialData();
}
