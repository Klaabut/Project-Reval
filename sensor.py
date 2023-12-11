import RPi.GPIO as GPIO
import ntplib
import datetime
import time
import threading
from multiprocessing import Process
from multiprocessing import Value
import statistics
import os


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


def get_internet_speed():
    while True:
        os.system("speedtest-cli --secure")
    
def sync_time_with_ntp_server(ntp_server, i):
    global ntp_synced
    j = 0;
    #command = "speedtest-cli --secure"
    command2 = "sudo ntpdate ntp.ttu.ee > /dev/null 2>&1"
    filename = "5_12_sensor_testing_ntp_1meg.txt"
    with open(filename, 'a') as f:
         f.write("\nTest algab\n")
         f.close()
    #os.system(f"{command} >> {filename}")
    while True:
        ntp_client = ntplib.NTPClient()
        current_timelast = time.time_ns()
        response = ntp_client.request(ntp_server)
        try:
             if(os.system(f"{command2} >> {filename}") != 0):
               print("Ei saanud ühendust\n")
             else:
                #print("Saime ühenduse\n")
                if j == 0:
                   ntp_synced.value = True
                   j = 1
        except Exception as e:
                print("An error occurred: ", e)           
        #precise_time = datetime.datetime.utcfromtimestamp(response.tx_time)
        #print(f"Time synchronized with {ntp_server}: {precise_time}")
        
        #microseconds_since_last_second = current_time_ns() % 1_000_000
        time_difference = current_timelast - time.time_ns() 
        #print(f"ajaerinevus {time_difference}")
        #time_difference_mc = time_difference // 1000
        #current_time_remaining_ns = time_difference % 1000
        #print(f"Erinevus mikrosekundites on  {time_difference_mc} ja nanosekundites {time_difference}\n")
        i = i + 1



def start_led_blink(i):
    #global ntp_synced
    while 1:
        #current_time_ns = time.time_ns()
        #even_second = current_time_ns // 1e9 % 2 != 0
        current_time = datetime.datetime.now()
        even_second = current_time.second % 2 != 0
        if even_second:
            current_time_ns = time.time_ns()
            #print(current_time_ns)
            nanoseconds_since_last_second = current_time_ns % 1_000_000_000 #get nanoseconds that have passed from last second
            sleep_ns(1000000000 - nanoseconds_since_last_second) #sleep until next second where ideally nanoseconds are 00
            current_time_ns = time.time_ns()
           # print(current_time_ns)
            # Turn on the LED
            
            GPIO.output(led_pin, GPIO.HIGH)
            sleep_ns(200000000)
            #time.sleep(0.4)  # LED on for 0.2 seconds (nanoseconds precision)
            GPIO.output(led_pin, GPIO.LOW)
            sleep_ns(1000000000) 
            #time.sleep(1.2) # Wait for the next second
            i = i+1
            with open("blink_and_ntp_times_black3.txt", "a") as file:
                file.write(f"Blink count: {i}, NTP time: {current_time_ns}\n")
def start_timer():
    with open("5_12_sensor_testing_1meg.txt", "a") as file:
        file.write("uus test\n")
        while True:
            if GPIO.input(signal_pin) == GPIO.LOW:
                current_time_ns = time.time_ns()
                file.write(f"NTP time: {current_time_ns}\n")
                file.flush()
                current_time_s = current_time_ns / 1_000_000_000
                #print(f"Signal Detected: {current_time.strftime('%S.%f')} (down to microseconds)")
                if current_time_s % 2 != 0:
                    delay = current_time_ns % 1_000_000_000
                    file.write(f"Arvutatud delay: {delay}\n")
                    file.flush()
                    print(f"\rdelay: {delay}ns")
                else:
                    print("delay suurem kui sekund")
   
                sleep_ns(800000000)  # Check every 0.1 seconds




ntp_synced = Value('b', False)
if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    ntp_server = "ntp.ttu.ee"
    i = 0
    j = 0
    sync_process = Process(target=sync_time_with_ntp_server, args=(ntp_server, i,))
    led_process = Process(target=start_led_blink, args=(i,))
    #net_process = Process(target=get_internet_speed)
    timer_process = Process(target=start_timer)
    sync_process.start()
    timer_process.start()
    #net_process.start()
    #global ntp_synced
    while j == 0:
        if ntp_synced.value == True:
            led_process.start()
            j = 1
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
