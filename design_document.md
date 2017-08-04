#Generic Design Document — Food Computer

There are multiple systems for the food computer.

 1. Operations
 2. Data Storage
 3. Analytics/Logging
 4. Visualization (UI/UX)

##Operations:
The bare minimum for the food computer are its core operations. It needs to be able to stabilize and modify the environment inside of the system. We will first cover the control of the sensors then the stabilization of the environment and lastly modification of the environment.

List of python class objects:

1. Environment Class — A wrapper for environmental settings with sane defaults.
2. Communication Class — A class for connecting to an Arduino
3. Environmental Control Class — A class for holding the environment at a specific setting
4. Environmental Pattern Class — A class for changing the environment to follow a specified pattern. (Recipe)

The communication and utilization of sensors and physical devices will be handled entirely a single python class. This class will encapsulate devices completely providing a simple API for the rest of the application. This class will be responsible for communication with an Arduino. Each instance of this class/object will be tied to a specific Arduino device. This will allow the application to communicate with multiple greenhouses at once if need be. This class will also offer a mock Arduino type to connect to for testing purposes. 

The stabilization of the environment will be handled by a python class whose sole responsibility will be responding to and predicting changes to the environment inside of the greenhouse. This class will be tied to a specific communication device class. It will provide a single external method of setting the environment of the inside of the greenhouse to a specific value. This class will attempt to maintain this value for the duration of the application or until updated again. When updating the environment a time scale may be specified to attempt to control the rate of change of the environment. This value will not be strictly adhered to as the system may not be capable of modify certain values, such as water temperature, quickly.


##Data Storage

Data storage will be a challenge for the system. This project will use both influxdb and postgres. The requirement of two databases provides the best of both of the databases but comes at the cost of higher maintenance. The databases will likely be stored together on the UI host to keep a single version of truth and to make the process of adding more greenhouses simpler. 

##Analytics / Logging

Analytics and logging are important for verification of environmental patterns and for learning. There are a few components to analytics and logging. The main principle of logging is that there must be something to log and there must be something to collect and transform the logs into something useful.

List of python class objects:

1. Environmental Control Class — from above, needs special logging to send out data.
2. Log Gathering Class — A class for gathering log files and transforming them into a format that can be input into a database in a useful fashion.
3. Database Connector — A class for taking useful logged objects and putting them in a database (influxdb, postgres)

The environmental control class will require an addition of a special logger that will output to its own log file. This will allow the log gathering class to more easily gather log files without having to parse out useless data. 

The log gathering class will be responsible for reading the log files produced by the environmental control class and transforming them into a useable form for input into the database. This class will be responsible for separating the logs by their respective greenhouses as well as separating via their obvious differences. e.g. water temp vs air temp.

The database connector class will be responsible for taking logs from the log class and pushing them into the proper databases (influxdb and possibly postgres). The database connector should be fairly lightweight as the majority of the heavy lifting should be performed by the log gathering class. 

##Visualization (UI/UX)

Visualization of the statuses of the various greenhouses is extremely important to the end user. This is the main way that most people will like to see information about their greenhouse. Visualization can be broken into multiple parts, the UI (data visualization), UI (camera data), and the UX (controls). This will most likely be handled by a Django application. This will be convent as Django supports multiple database types. The UI (camera data) will be the most difficult part to engineer as the camera does not need to be explicitly collected by the environmental system. This suggests that their should perhaps be a daemon for the camera and for exposing the local data from a greenhouse. This idea seems contrary to other design decisions for this project and as such the camera control will likely be integrated into the environmental systems. 

The UI (data visualization)  will be performed by graphing via influxdb. This can be provided by passing grafana into the system as an iframe. If this is not easily, programatically configurable other options will be sought, such as chart.js although this is less desirable. The specification of which greenhouse is being visualized or for overlaying them is not yet determined as I have not fully explored all of the options in this area. 

The UI (camera data) will be used by connecting to a web endpoint provided by either operations or by logging and analytics. The camera will be easy to display as it is a simple img tag in html. This will be easy on the fronted of the UI. 

The UX (controls) will be the most difficult part of the entire build. The controls will use sockets to communicate with the environmental control systems. This will not be encrypted but will be authenticated at very least. Using sockets will allow for the Django application to directly send messages and receive confirmation from the environmental control systems even if there are many of them on the network of devices. 

##Security

As an enterprise grade system this project will need to identify and mitigate threats to the greenhouses and to the datastore host. Ideally the system would use mTLS for authentication but this adds quite a bit of time to the build process as well as making it more difficult for greenhouses to be added to the system. More realistically the system will use https with authentication to connect to the databases allowing for a simple creation of new databases. 

##Implementation

The databases will need to be up and running first. These will be docker containerized databases on the UI host. This will allow that host to be set up with a single run of docker compose. This will be ideal.  After the databases and UI are up and running it will be time to add greenhouses. Adding a greenhouse application should also be as simple as docker compose up. Although it will use docker-compose it will be unlikely to be more than one docker container for the operations and logging. This docker-compose will require the db names and passwords for the host. The system would be best with implementing zeroconf for discovery of the UI host and databases. This should have the option to be overridden if someone desires since they may be running multiple UI hosts. e.g. (production and development) or (remote host). This setup would allow for a UI host to have zero or more green houses; this puts a strict requirement to be dynamic without restarting on the UI. 







