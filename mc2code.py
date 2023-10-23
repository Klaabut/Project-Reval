from gpiozero import LED
import ntplib
import datetime

def sync_time_with_ntp_server(ntp_server):
    try:
        # Create an NTP client
        ntp_client = ntplib.NTPClient()

        # Send a request to the NTP server
        response = ntp_client.request(ntp_server)

        # Calculate the precise time
        precise_time = datetime.datetime.utcfromtimestamp(response.tx_time)

        # Print the precise time
        print(f"Time synchronized with {ntp_server}: {precise_time}")

    except Exception as e:
        print(f"Failed to synchronize time: {e}")

if __name__ == "__main__":
    # Use a highly accurate NTP server (replace with a suitable server)
    ntp_server = "ntp.ttu.ee"
    sync_time_with_ntp_server(ntp_server)