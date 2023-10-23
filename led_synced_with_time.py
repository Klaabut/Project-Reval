import RPi.GPIO as GPIO
import ntplib
import datetime
import time
from time import sleep
# Ignore warning for now
GPIO.setwarnings(False) 
# Set the GPIO mode to BOARD mode
# Pin to which LED is connected
led_pin = 7  
# Setup the LED pin as an output
GPIO.setup(led_pin, GPIO.OUT)
def sync_time_with_ntp_server(ntp_server):
    try:
        while True:
        # Create an NTP client
         ntp_client = ntplib.NTPClient()

        # Send a request to the NTP server
         response = ntp_client.request(ntp_server)

        # Calculate the precise time
         precise_time = datetime.datetime.utcfromtimestamp(response.tx_time)
         seconds = precise_time.second
         print(f"Time synchronized with {ntp_server}: {precise_time}")
         print(f"seconds: {seconds}")
         #if time ends with five blink LED
         if seconds % 10 == 5:
             GPIO.output(led_pin, GPIO.HIGH)
             sleep(1)
    except Exception as e:
        print(f"Failed to synchronize time: {e}")

if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    ntp_server = "ntp.ttu.ee"
    sync_time_with_ntp_server(ntp_server)
