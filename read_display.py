#!/usr/bin/env python3
import logging
import smbus
from time import sleep, strftime
from datetime import datetime
from threading import Thread
from Display_src.LCD1602 import CharLCD1602
from RFID_src.SimpleMFRC522 import SimpleMFRC522  # Import the RFID library
import rdm6300

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

def read_simple_mfrc522():
    while True:
        try:
            id, text = reader.read_no_block()
            if id not in [None, ''] and text not in [None, '']:
                logging.debug(f'RFID tag read: ID={id}, Text={text}')
                display_rfid_data(id, text)
        except Exception as e:
            logging.error(f'Error reading SimpleMFRC522: {e}')
        sleep(1)

def read_rdm6300():
    while True:
        try:
            rdm_card = rdm_reader.start()
            if rdm_card:
                logging.debug(f'RDM6300 card read: ID={rdm_card.value}')
                display_rfid_data(rdm_card.value, "RDM6300 Card")
        except Exception as e:
            logging.error(f'Error reading RDM6300: {e}')
        sleep(1)

def loop():
    lcd1602.init_lcd()
    logging.info('LCD initialized')
    display_cpu_and_time()
    prompt_for_rfid()

    # Start threads for reading from both readers
    simple_thread = Thread(target=read_simple_mfrc522)
    rdm_thread = Thread(target=read_rdm6300)
    simple_thread.start()
    rdm_thread.start()

    # Keep the main thread alive
    while True:
        display_cpu_and_time()
        sleep(10)

def destroy():
    lcd1602.clear()
    logging.info('LCD cleared')

class RDM6300Reader(rdm6300.BaseReader):
    def card_inserted(self, card):
        logging.info(f"RDM6300 card inserted {card}")
        display_rfid_data(card.value, "RDM6300 Card")

    def card_removed(self, card):
        logging.info(f"RDM6300 card removed {card}")

    def invalid_card(self, card):
        logging.info(f"RDM6300 invalid card {card}")

rdm_reader = RDM6300Reader('/dev/ttyS0')

if __name__ == '__main__':
    logging.info('Program is starting ...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        logging.info('Program terminated by user')