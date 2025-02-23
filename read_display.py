#!/usr/bin/env python3
import logging
import smbus
from time import sleep, strftime
from datetime import datetime
from Display_src.LCD1602 import CharLCD1602
from RFID_src.SimpleMFRC522 import SimpleMFRC522  # Import the RFID library

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

lcd1602 = CharLCD1602()
reader = SimpleMFRC522()  # Initialize the RFID reader

def get_cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as tmp:
        cpu = tmp.read()
    logging.debug(f'CPU temperature read: {cpu}')
    return '{:.2f}'.format(float(cpu) / 1000) + ' C '

def get_time_now():
    current_time = datetime.now().strftime('    %H:%M:%S')
    logging.debug(f'Current time: {current_time}')
    return current_time

def display_cpu_and_time():
    lcd1602.clear()
    lcd1602.write(0, 0, 'CPU: ' + get_cpu_temp())
    lcd1602.write(0, 1, get_time_now())

def prompt_for_rfid():
    lcd1602.clear()
    lcd1602.write(0, 0, 'Place RFID tag')
    logging.info('Waiting for RFID tag')

def display_rfid_data(id, text):
    lcd1602.clear()
    lcd1602.write(0, 0, 'RFID ID:')
    lcd1602.write(0, 1, str(id))
    sleep(2)
    lcd1602.clear()
    lcd1602.write(0, 0, 'Data:')
    lcd1602.write(0, 1, text)
    sleep(2)

def loop():
    lcd1602.init_lcd()
    logging.info('LCD initialized')
    while True:
        display_cpu_and_time()
        id, text = reader.read()
        if id not in [None, ''] and text not in [None, '']:
            logging.debug(f'RFID tag read: ID={id}, Text={text}')
            display_rfid_data(id, text)
        sleep(1)

def destroy():
    lcd1602.clear()
    logging.info('LCD cleared')

if __name__ == '__main__':
    logging.info('Program is starting ...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        logging.info('Program terminated by user')