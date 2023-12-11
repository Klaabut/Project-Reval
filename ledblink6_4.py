import RPi.GPIO as GPIO
import datetime
from datetime import datetime, timezone, timedelta
import time
from multiprocessing import Process
from multiprocessing import Value
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
    
def write_to_file(text):
   filename = "test.txt"
   with open(filename, 'a') as f:
         f.write(f"{text}\n")

    
def sync_time_with_ntp_server(i):
    global ntp_synced
    global end_work
    j = 0;
    #command = "speedtest-cli --secure"
    command2 = "sudo ntpdate ntp.ttu.ee"
    filename = "1meg_green_ntp.txt"
    with open(filename, 'a') as f:
         f.write("\nTest algab\n")
         f.close()
    #os.system(f"{command} >> {filename}")
    while end_work.value == False:
        process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
         final = output.decode('utf-8')
         if j == 0:
            ntp_synced.value = True
            j = 1
         print(final)
         write_to_file(final)
        else:
            print(error.decode())




def start_led_blink(i):
    #global ntp_synced
    # with open("1meg_green_blink.txt", "w") as file:
      # file.write("Test algas\n")
      # file.flush()
      global end_work
      while i < 3:
        current_time = datetime.now()
        even_second = current_time.second % 2 != 0
        #if it is even second go to the if loop otherwise start the while loop over again
        if even_second:
            current_time_ns = time.time_ns()
            #get nanoseconds since last even second
            nanoseconds_since_last_second = current_time_ns % 1_000_000_000
            #wait until next second starts
            sleep_ns(1000000000 - nanoseconds_since_last_second)
            current_time_ns = time.time_ns()
            # Turn on the LED
            GPIO.output(led_pin, GPIO.HIGH)
            sleep_ns(200000000)
            GPIO.output(led_pin, GPIO.LOW)
            sleep_ns(1000000000) 
            #increase the counter
            i = i+1
            seconds = current_time_ns / 1e9
            seconds+=7200
            nanoseconds =  current_time_ns % 1e9 
            dt = datetime.fromtimestamp(seconds,tz=timezone.utc)
            dt+=timedelta(microseconds=nanoseconds//1000)
            text = f"Blink count: {i}, NTP time: {current_time_ns} {dt}\n"
            write_to_file(text)
 
      end_work.value = True

#global value that gives info about if time has been synced with ntp server
ntp_synced = Value('b', False)
end_work = Value('b', False)
if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    i = 0
    j = 0
    k = 0
    text = "uus test"
    sync_process = Process(target=sync_time_with_ntp_server, args=(i,))
    led_process = Process(target=start_led_blink, args=(i,))
    write_process = Process(target=write_to_file, args=(text,))
    sync_process.start()
    write_process.start()
    while j == 0:
        if ntp_synced.value == True:
            led_process.start()
            j = 1
    while k == 0:
        if end_work.value == True:
            print("end end end")
            exit()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

