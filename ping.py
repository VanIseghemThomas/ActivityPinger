from pythonping import ping #pip install pythonping
import time
import csv

TARGET = '192.168.0.1'   # Target IP
TIMEOUT =  5    # Interval to ping and log in seconds
N_PACKETS = 3   # Number of packets to send on ping request

start = time.time()
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start))
filename = f'activity_{timestamp}.csv'

# Create new CSV file
with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'target', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

# Main loop
while True:
    # Check for time interval
    if time.time() - start >= TIMEOUT:
        start = time.time() 
        response = ping(TARGET, verbose=False, count=N_PACKETS)
        #print(response.packets_lost)

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))

        # Check if host has gone offline by dropped packets
        if(response.packets_lost == 1):
            print(f"{timestamp}: Host went offline")
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'target', 'online']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'timestamp': timestamp, 'target': TARGET, 'online': 0})

        else:
            print(f"{timestamp}: Host online")
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'target', 'online']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'timestamp': timestamp, 'target': TARGET, 'online': 1})