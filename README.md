# Raspberry Pi Weather Station - Client

This repo contains the Raspberry Pi client of the weather station. The python client measures the temperature and the humidity, requests the gps coordinates and sends it to the server's REST API.

[Working demo]

## Hardware

* Raspberry Pi 2 Model B
* Microstack L80 GPS
* DHT11 Temperature and Humidity sensor

## Prerequisites
* [wiringPi]
* [Microstack™ Node libraries for Python 3]

## Connection

* GPS: Serial port
  * MTXSRX  PIN#08 GPIO14 (TXD0)
  * MRXSTX - PIN#10 GPIO15 (RXD0)
* Sensor: PIN#07 GPIO04


## Running
You need root privileges to run the app:
```sh
$ sudo python3 [git-repo]/client.py
```
## Running in the background
You can run the client in the background with the command screen:
```sh
$ sudo screen -dm -S pi-weather-station-client python3 [git-repo]/client.py
```
Install screen If you haven't already:
```sh
$ sudo apt-get update
$ sudo apt-get install screen
```
To run the app at boot insert the following command to /etc/rc.local:
```sh
screen -dm -S pi-weather-station-client python3 [git-repo]/client.py
```
To access the screen:
```sh
$ sudo -i
$ screen -DR
```
You can leave the screen without actually closing the app by pressing Ctrl+A+D.
## (Optional) Compiling
You can build the src/read_sensor_temp.c file with:
```sh
$ cd [git-repo]/src
$ make
```
## Todos

* Add Code Comments
* Better Logging
* Add config file (ex: server address, sensor pin, etc.)
* Add command line parameters (ex: --log debug, --no-gps, --server address)

### Version
0.1




   [Server]: <https://github.com/FlipEverything/pi-weather-station-server>
   [wiringPi]: <http://wiringpi.com/>
   [Microstack™ Node libraries for Python 3]: <http://www.farnell.com/datasheets/1860443.pdf>
   [Working demo]: <https://lddsystems.eu/weather/>

