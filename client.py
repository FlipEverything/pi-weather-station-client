#!/usr/bin/python3
import time
import logging
import os
import subprocess
import http.client
import urllib.parse
import datetime
import json
import microstacknode.gps.l80gps

def read_gps_data():
    logging.debug('Reading GPS data...');
    try:
        gps = microstacknode.gps.l80gps.L80GPS()
        return gps.gpgll;
    except microstacknode.gps.l80gps.NMEAPacketNotFoundError as e:
        return 0

def read_temp_sensor_data():
    logging.debug('Reading weather sensor data...')
    try:
        output = subprocess.check_output([os.getcwd() + '/bin/read_sensor_temp'])
        output = output.decode();
        output = output.split(',');
        weather = dict();
        weather['humidity'] = float(output[0])
        weather['temperature'] = float(output[1])
        return weather
    except subprocess.CalledProcessError as e:
        raise SystemExit

def send_data_to_server(weather, gpgll):
    logging.debug('Sending data to server...')
    params = urllib.parse.urlencode({'date': datetime.datetime.now(), 'gpsLongitude': gpgll['longitude'], 'gpsLatitude': gpgll['latitude'],
                               'temperature': weather['temperature'], 'humidity': weather['humidity']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = http.client.HTTPSConnection("lddsystems.eu")
    conn.request("POST", "/weather/api/measure", params, headers)
    response = conn.getresponse()
    logging.debug('  Server responded with', response.status, response.reason)
    data = response.read()
    conn.close()


if __name__ == '__main__':
    logging.basicConfig(filename=os.getcwd() +'/client.log',level=logging.DEBUG)
    logging.debug('Application started')
    prev_weather = dict();
    prev_weather['humidity'] = 0;
    prev_weather['temperature'] = 0;
    prev_gpgll = dict();
    prev_gpgll['latitude'] = 0;
    prev_gpgll['longitude'] = 0;


    while True:
        gpgll = read_gps_data()
        if (gpgll != 0) :
            logging.debug('  Latitude: {0:0.8f}, Longitude: {1:0.8f}'.format(gpgll['latitude'], gpgll['longitude']))

            weather = read_temp_sensor_data();
            logging.debug('  Humidity: {0:0.2f}, Temperature: {1:0.2f}'.format(weather['humidity'], weather['temperature']))

            if weather['humidity'] != prev_weather['humidity'] and weather['temperature'] != prev_weather['temperature'] and gpgll['longitude'] != prev_gpgll['longitude'] and gpgll['latitude'] != prev_gpgll['latitude']:
                send_data_to_server(weather, gpgll)
                prev_weather = weather;
                prev_gpgll = gpgll;
            else:
                logging.debug('Not sending data - nothing changed.')
        else:
            logging.debug(' Timed out before valid GPGLL')

        time.sleep(1)

