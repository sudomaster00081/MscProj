from scapy.all import *
import os
from tqdm import tqdm

def split_pcap(input_file):
    # Create a directory to store the cropped pcap files if it doesn't exist
    if not os.path.exists("cropped"):
        os.makedirs("cropped")

    # Get the base name of the input file
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Define the time interval (5 seconds)
    interval = 5

    # Initialize variables for file index and packet count
    file_index = 1
    packet_count = 0

    # Open the pcap file in read mode
    with PcapReader(input_file) as pcap_reader:
        # Initialize tqdm progress bar
        progress_bar = tqdm(desc=f"Splitting {input_file}", unit=" packets")

        # Initialize list to store packets for the current interval
        interval_packets = []

        # Loop through each packet in the pcap file
        for packet in pcap_reader:
            # Calculate the elapsed time since the start of the capture
            elapsed_time = packet.time - interval_packets[0].time if interval_packets else 0

            # Check if elapsed time exceeds the interval
            if elapsed_time >= interval:
                # Write the interval packets to a new pcap file
                output_file = f"cropped/{base_name}_{file_index}.pcap"
                wrpcap(output_file, interval_packets)

                # Reset variables for the next interval
                interval_packets = [packet]
                file_index += 1
            else:
                # Add the packet to the current interval
                interval_packets.append(packet)

            # Increment packet count
            packet_count += 1

            # Update the progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

    print(f"Split {input_file} into {file_index} parts successfully.")

# Get a list of all .pcap files in the current directory
pcap_files = [f for f in os.listdir() if f.endswith('.pcap')]

# Iterate over each .pcap file and split it
for pcap_file in pcap_files:
    split_pcap(pcap_file)
