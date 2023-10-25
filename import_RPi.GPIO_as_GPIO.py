import RPi.GPIO as GPIO
import ntplib
import datetime
import time
import threading

# Ignore warning for now
GPIO.setwarnings(False)

# Set the GPIO mode to BOARD mode
GPIO.setmode(GPIO.BOARD)

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
            print(f"Time synchronized with {ntp_server}: {precise_time}")

            time.sleep(5)  # Wait for 5 seconds before syncing again
    except Exception as e:
        print(f"Failed to synchronize time: {e}")

def blink_led():
    try:
        while True:
            current_time = time.time()
            milliseconds = int((current_time * 1000) % 2000)

            if milliseconds < 1000:  # LED on for the first second
                GPIO.output(led_pin, GPIO.HIGH)
            else:  # LED off for the second second
                GPIO.output(led_pin, GPIO.LOW)

            time.sleep(0.1)  # Check every 0.1 second for precise timing
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    ntp_server = "ntp.ttu.ee"

    ntp_thread = threading.Thread(target=sync_time_with_ntp_server, args=(ntp_server,))
    led_thread = threading.Thread(target=blink_led)

    ntp_thread.start()
    led_thread.start()

    ntp_thread.join()
    led_thread.join()
