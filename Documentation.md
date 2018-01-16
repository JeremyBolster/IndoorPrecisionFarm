# Docs
===============

## Arduino
******************

### Drivers

Sensor drivers for this project are implemented in C++. This is similar to the Arduino code examples that can be found for most hobbyist sensors. It also allows for maximum extensibility. 

#### Interface

The driver interface is quite simple to use. Two methods must be implemented for any metric that is collected by the sensor.

1. void setup_<metric_name>(void);
2. float get_<metric_name>(void);

The setup code will be called once at the boot time and then it will not be called again. The get method will be called at regular intervals. These intervals are dictated by the frequency of the poll command.

## Backend
******************

### Climate Control System

#### Overview

The climate control system is the main focus of the backend application. The majority of the other pieces of the backend are related to data transfer. 

The main goal of the climate control system is to control the climate inside of the precision farm based on the currently selected At a high level the climate control system takes in the current status of the farm based on the sensor data and toggles the control devices, such as the heater, to manipulate those values to the desired values (from the climate pattern). 

The EnvironmentalControl class takes the sensor values as an Environment object. The Environment object serves as a data storage medium for the sensor data. It is updated via the Greenhouse (TODO make this Farm) class. It is updated externally from the EnvironmentalControl class as the EnvironmentalControl class should not contain logic for gathering sensor data. The climate control system does contain a reference to the communitcation object; however this is necessary as it needs to toggle devices within the farm. 

#### Climate Patterns

The climate patterns used by this system are heavily inspired and in some cases, compatible with the MIT Food Computer climate recipies. The interesting part of the pattern is the operations section. This section contains a list of cycles. Cycles have two components (A more generic solution should be implemented in the future), day and night. Each cycle component has a time and environment setting. The time setting, called 'hours', is the amount of time to keep the climate at the environment setting. The environment setting contains values for environmental variables. Note that all of the variables supported by this application do not need to be specified. If none are specified default values will be applied (CAUTION: DEFAULT VALUES MAY CAUSE ERRORS IF THEY ARE NOT EXPECTED). 

###### An example of a climate pattern's operation section:

```YAML
operations:
- cycles: 2
  name: early
  day:
    hours: 0.01
    environment:
      waterTemp: 24
      lux: 1200
      pH: 6
      humidity: 45
      airTemp: 25
      co2: 1000
  night:
    hours: 0.01
    environment:
      waterTemp: 23
      lux: 0
      pH: 6
      humidity: 75
      airTemp: 22
      co2: 600
```

### Arduino Communication

Communication with the Arduino is completely encapsulated in the communication library. This means that a device other than an Arduino can be used as the source of the sensor data with the addition of a new class. The type of communication object that is initialized is determined by the command flag `--device` and the logic for initializing that class is contained within run.py. 

The Arduino communication uses the `PyCmdMessenger` library to communicate with the Arduino. This library handles all of the buffering and conversion of types. It works in conjunction with `CmdMessenger` running on the Arduino. 

The communication interface provides three external methods for external components to use to interact with the physical components of the farm. The `send_msg` method is the lowest level interface as it requires some knowledge of the underlying implementation. 

```python
    def send_msg(self, msg: List[str]) -> bool:
        """
        This method sends a message as a command to the specified sensor. It returns a boolean representing whether it
        was successful or not.
        :param msg: Message to send to the sensor
        :return: Success status of the message
        """

    def receive_msg(self, device: str) -> Dict[float, float]:
        """
        This method gets the stored messages for a given sensor from the queue.
        :param device: The device to receive messages for
        :return: The messages of a given sensor. This is a dictionary mapping from the timestamp to the 'value'
        """

    def toggle_device(self, device: str, on_off: OnOff) -> bool:
        """
        This method toggles the specified device to the specified status. It returns the success of the toggle as a
        boolean.
        :param device: Name of the device to toggle as a string.
        :param on_off: Desired status of the device.
        :return: The success of the toggle.
        """
```
### REST endpoint

| Endpoint           | Request Type | Description |
| :----------------- |:------------:| :-----      |
| /                  | [GET]        | Returns basic information about the farm |
| /api               | [GET]        | Returns a list of the supported api versions of the farm |
| /api/<version>     | [GET]        | Returns a complete list of endpoints for the specified version of the api |
| /api/v1/climate    | [GET]        | Returns the current climate values of the farm
| /api/v1/pattern    | [GET]        | Returns the current pattern that the farm is executing
| /api/v1/pattern    | [POST]       | Set the current climate pattern
| /api/v1/status     | [GET]        | Returns various status reports, including the current elapsed time and total time
| /api/v1/image      | [GET]        | Returns the timestamp of the last image taken and a direct link to that image
| /api/v1/image/view | [GET]        | Returns the last image taken



### Webcam Photos

Not yet implemented!!!!!

## Frontend
******************

