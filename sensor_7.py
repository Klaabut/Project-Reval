import RPi.GPIO as GPIO
import ntplib
import datetime
import time
import threading
from multiprocessing import Process
from multiprocessing import Value
import statistics
import os
import subprocess

# Ignore warning for now
GPIO.setwarnings(False)

# Set the GPIO mode to BOARD mode
GPIO.setmode(GPIO.BOARD)

# Pin to which LED is connected
led_pin = 3

# Pin for signal detection
signal_pin = 8  # Replace with the actual GPIO pin number

# Setup the LED pin as an output
GPIO.setup(led_pin, GPIO.OUT)

# Setup the signal pin as an input with pull-down resistor
GPIO.setup(signal_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def sleep_ns(duration_ns):
    start_time = time.time_ns()
    while time.time_ns() - start_time < duration_ns:
        pass
    end_time = time.time_ns()
    actual_delay = end_time - start_time
    #print(f"Tahetud: {duration_ns},  Real: {actual_delay}")


def write_to_file(text):
   filename = "sys_sensor_omaviide_nice_topelt_250.txt"
   with open(filename, 'a') as f:
         f.write(f"{text}\n")

def sync_time_with_ntp_server(i):
    global ntp_synced
    global end_work
    j = 0;
    command2 = "sudo ntpdate ntp.ttu.ee"
    write_to_file("Test algab\n")
    while True:
        process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
         final = output.decode('utf-8')
         write_to_file(final)
        else:
            print(error.decode())


def start_timer():
        while True:
            if GPIO.input(signal_pin) == GPIO.LOW:
                current_time_ns = time.time_ns()
                text = f"NTP time: {current_time_ns}\n"
                write_to_file(text)
                current_time_s = current_time_ns / 1_000_000_000
                current_time_full = int(current_time_s)
                text = f"Sekund: {current_time_full}\n"
                write_to_file(text)
                delay = 0
                if current_time_full % 2 == 0:
                    delay = current_time_ns % 1_000_000_000
                    text = f"Arvutatud delay: {delay}\n"
                    write_to_file(text)
                    print(f"\rdelay: {delay}ns")
                else:
                    delay = current_time_ns % 1_000_000_000
                    delay+= 1_000_000_000
                    print(f"\rdelay: {delay}ns")
                    text = f"Arvutatud delay: {delay}\n"
                    write_to_file(text)
                sleep_ns(800000000)  # Check every 0.1 seconds




ntp_synced = Value('b', False)
if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    ntp_server = "ntp.ttu.ee"
    i = 0
    j = 0
    sync_process = Process(target=sync_time_with_ntp_server, args=(i,))
    timer_process = Process(target=start_timer)
    sync_process.start()
    timer_process.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

