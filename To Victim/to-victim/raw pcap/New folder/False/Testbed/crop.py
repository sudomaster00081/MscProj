from scapy.all import *
import os

def split_pcap(input_file):
    # Create a directory to store the cropped pcap files if it doesn't exist
    if not os.path.exists("cropped"):
        os.makedirs("cropped")

    # Load the pcap file
    packets = rdpcap(input_file)

    # Get the first packet's timestamp
    start_time = packets[0].time

    # Define the time interval (5 seconds)
    interval = 5

    # Initialize variables for packet counts and file index
    packet_count = 0
    file_index = 1

    # Initialize a list to store packets for the current interval
    interval_packets = []

    # Loop through each packet in the pcap file
    for packet in packets:
        # Calculate the elapsed time since the start of the capture
        elapsed_time = packet.time - start_time

        # Check if elapsed time exceeds the interval
        if elapsed_time >= interval:
            # Write the interval packets to a new pcap file
            output_file = f"cropped/{input_file.split('.')[0]}_{file_index}.pcap"
            wrpcap(output_file, interval_packets)

            # Reset variables for the next interval
            interval_packets = []
            start_time = packet.time
            file_index += 1

        # Add the packet to the current interval
        interval_packets.append(packet)
        packet_count += 1

    # Write the remaining packets to a pcap file
    output_file = f"cropped/{input_file.split('.')[0]}_{file_index}.pcap"
    wrpcap(output_file, interval_packets)

    print(f"Split {input_file} into {file_index} parts successfully.")

# Get a list of all .pcap files in the current directory
pcap_files = [f for f in os.listdir() if f.endswith('.pcap')]

# Iterate over each .pcap file and split it
for pcap_file in pcap_files:
    split_pcap(pcap_file)
