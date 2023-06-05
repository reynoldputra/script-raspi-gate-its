#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time

LED_GREEN = 11
LED_RED = 13
LED_BLUE = 15
buzzer_pin = 7

log_file = "log.txt"

def printToFile(text):
    with open(log_file, "a") as f:
        f.write(text)
        f.write("\n")

GPIO.setwarnings(False)
reader = SimpleMFRC522()


def green():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.output(LED_GREEN, GPIO.HIGH)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.output(LED_BLUE, GPIO.LOW)

def red():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.output(LED_RED, GPIO.HIGH)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.output(LED_BLUE, GPIO.LOW)

def blue():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.output(LED_BLUE, GPIO.HIGH)


def buz():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.output(buzzer_pin, GPIO.HIGH) 
    time.sleep(0.01)
    GPIO.output(buzzer_pin, GPIO.LOW)

try:
    while True:
        blue()
        printToFile("=================")
        printToFile("Scanning card ...")
        id, text = reader.read()
        printToFile(id)
        printToFile("Request to api ...")
        url = "http://10.15.43.100:3000/masuk"
        data = {
            'card_id' : id,
            'gate_id' : 5
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        _res = requests.post(url, data=data, headers=headers)
        printToFile(_res.text)
        status = _res.text
        if status == "1":
            printToFile("Success to read")
            green()
            buz()
        else:
            printToFile("Failed to read")
            red()
            buz()
            buz()
        time.sleep(0.3)
        GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
