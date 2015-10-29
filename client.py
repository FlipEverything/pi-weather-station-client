#!/usr/bin/python3
import logging
import time
import os
import subprocess
import http.client
import urllib.parse
import datetime
import json
import microstacknode.gps.l80gps
from socket import timeout

logging.basicConfig(filename='/var/log/pi-weather-station-client.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

def read_gps_data():
    logging.debug('Reading GPS data...');
    try:
        gps = microstacknode.gps.l80gps.L80GPS()
        logging.debug('Latitude: {0:0.8f}, Longitude: {1:0.8f}'.format(gps.gpgll['latitude'], gps.gpgll['longitude']))
        return gps.gpgll;
    except:
        logging.error('Timed out before valid GPGLL')
        return 0

def read_temp_sensor_data():
    logging.debug('Reading weather sensor data...')
    try:
        output = subprocess.check_output(['/home/pi/pi-weather-station-client/bin/read_sensor_temp'])
        output = output.decode();
        output = output.split(',');
        weather = dict();
        weather['humidity'] = float(output[0])
        weather['temperature'] = float(output[1])
        logging.debug('Humidity: {0:0.2f}, Temperature: {1:0.2f}'.format(weather['humidity'], weather['temperature']))
        return weather
    except subprocess.CalledProcessError as e:
        logging.error('Cannot read weather sensor')
        raise SystemExit

def send_data_to_server(weather, gpgll):
    logging.debug('Sending data to server...')
    params = urllib.parse.urlencode({'date': datetime.datetime.now(), 'gpsLongitude': gpgll['longitude'], 'gpsLatitude': gpgll['latitude'],
                               'temperature': weather['temperature'], 'humidity': weather['humidity']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    try:
        conn = http.client.HTTPSConnection("lddsystems.eu")
        conn.request("POST", "/weather/api/measure", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except (HTTPError, URLError) as error:
        logging.error('Data of %s not retrieved because %s\nURL: %s', name, error, url)
    except timeout:
        logging.error('socket timed out - URL %s', url)
    else:
        logging.debug('Server responded with ' + str(response.status) + ' ' + response.reason)


if __name__ == '__main__':
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
            weather = read_temp_sensor_data();
            if weather['humidity'] != prev_weather['humidity'] and weather['temperature'] != prev_weather['temperature'] and gpgll['longitude'] != prev_gpgll['longitude'] and gpgll['latitude'] != prev_gpgll['latitude']:
                send_data_to_server(weather, gpgll)
                prev_weather = weather;
                prev_gpgll = gpgll;
            else:
                logging.debug('Not sending data - nothing changed.')

        time.sleep(1)

