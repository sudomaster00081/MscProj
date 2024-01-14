import os
import scapy.all as scapy
import pandas as pd
from tqdm import tqdm

# Path to the directory containing the pcap files
directory_path = ''  # Replace with the path to your pcap files

# Function to extract features from packets
def process_packet(packet, packet_data):
    # Extract relevant features from the packet
    # You may need to adjust these based on your specific requirements
    src_ip = packet[scapy.IP].src
    dst_ip = packet[scapy.IP].dst
    protocol = packet[scapy.IP].proto
    packet_size = len(packet)

    # Add additional features as needed

    # Append data to the list
    packet_data.append([src_ip, dst_ip, protocol, packet_size])

# Iterate through pcap files in the 'to-victim' subdirectory
to_victim_path = os.path.join(directory_path, 'to-victim')
for file_name in tqdm(os.listdir(to_victim_path), desc="Processing pcap files", unit="file"):
    if file_name.endswith('.pcap'):
        file_path = os.path.join(to_victim_path, file_name)

        # List to store packet data for each pcap file
        packet_data = []

        # Process each packet in the pcap file
        scapy.sniff(offline=file_path, prn=lambda x: process_packet(x, packet_data))

        # Create a DataFrame from the collected packet data
        columns = ['Src_IP', 'Dst_IP', 'Protocol', 'Packet_Size']
        df = pd.DataFrame(packet_data, columns=columns)

        # Save the DataFrame to a CSV file with the same name as the pcap file
        csv_file_path = os.path.splitext(file_path)[0] + '_processed.csv'
        df.to_csv(csv_file_path, index=False)
