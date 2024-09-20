import network
import socket
import time
from machine import Pin
import sys

# WiFi Configuration
SSID = 'RaspberryPi_Eon'
PASSWORD = 'password'

# Morse Code Timing Definitions (in seconds)
UNIT = 0.2  # Duration of one unit
DOT_DURATION = UNIT
DASH_DURATION = 3 * UNIT
INTRA_CHAR_GAP = UNIT  # Gap between dots and dashes within a character
INTER_CHAR_GAP = 3 * UNIT  # Gap between characters
INTER_WORD_GAP = 7 * UNIT  # Gap between words

# Initialize WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

# Attempt to connect to WiFi
print('Connecting to WiFi...')
MAX_ATTEMPTS = 20
attempt = 0
while not station.isconnected() and attempt < MAX_ATTEMPTS:
    print(f'Attempting to connect... Try {attempt + 1}/{MAX_ATTEMPTS}')
    time.sleep(1)
    attempt += 1

if station.isconnected():
    print('Connection successful')
    print('Configuration:', station.ifconfig())
else:
    print('Failed to connect to WiFi')
    sys.exit()

# Initialize LED
LED_PIN = 2  # Change this if your LED is connected to a different pin
led = Pin(LED_PIN, Pin.OUT)


def blink(duration):
    """Blink the LED for the specified duration."""
    led.on()
    time.sleep(duration)
    led.off()


def parse_and_blink(morse_code):
    """  
    Parse the received Morse code string and blink the LED accordingly.    Supports dots (.), dashes (-), and spaces for gaps.    """
    print(f'Parsing Morse code: "{morse_code}"')
    for symbol in morse_code:
        if symbol == '.':
            blink(DOT_DURATION)
            time.sleep(INTRA_CHAR_GAP)
        elif symbol == '-':
            blink(DASH_DURATION)
            time.sleep(INTRA_CHAR_GAP)
        elif symbol == ' ':
            time.sleep(INTER_CHAR_GAP - INTRA_CHAR_GAP)  # Already waited INTRA_CHAR_GAP after symbol
        else:
            pass
    print('Finished parsing Morse code.')


def receive_and_process(sock):
    """Receive and process incoming Morse code messages."""
    try:
        while True:
            sock.settimeout(10.0)  # Timeout set to 10 seconds
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                morse_message = data.decode('utf-8').strip()
                print(f'Received message from {addr}: "{morse_message}"')

                if morse_message:
                    parse_and_blink(morse_message)

            except OSError as e:
                print("Socket timeout, no message received.")
    except KeyboardInterrupt:
        print("Script execution interrupted")
    finally:
        sock.close()
        print("Socket closed")

    # Initialize UDP Server


UDP_IP = '0.0.0.0'
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print('UDP server started and waiting for messages...')

receive_and_process(sock)
