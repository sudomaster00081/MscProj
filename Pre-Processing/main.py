import os
from scapy.all import sniff, IP, TCP
import scapy.utils
import pandas as pd
from tqdm import tqdm

# Path to the directory containing the pcap files
directory_path = ''  # Replace with the path to your pcap files

# Function to extract features from packets
def process_packet(packet, packet_data, previous_timestamp):
    # Extract relevant features from the packet
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol = packet[IP].proto
    packet_size = len(packet)
    timestamp = packet.time

    # Calculate inter-arrival time
    if previous_timestamp is not None:
        inter_arrival_time = timestamp - previous_timestamp
    else:
        inter_arrival_time = 0  # For the first packet

    # Extract additional features
    dst_port = packet.dport if TCP in packet and hasattr(packet[TCP], 'dport') else None
    
    # Corrected entropy calculation using payload
    try:
        payload_entropy = scapy.utils.entropy(str(packet.payload))
    except AttributeError:
        payload_entropy = None

    # Append data to the list
    packet_data.append([src_ip, dst_ip, protocol, packet_size, inter_arrival_time, dst_port, payload_entropy])

    return timestamp

# Iterate through pcap files in the 'to-victim' subdirectory
to_victim_path = os.path.join(directory_path, 'to-victim')
for file_name in tqdm(os.listdir(to_victim_path), desc="Processing pcap files", unit="file"):
    if file_name.endswith('.pcap'):
        file_path = os.path.join(to_victim_path, file_name)

        # List to store packet data for each pcap file
        packet_data = []
        previous_timestamp = None

        # Process each packet in the pcap file
        sniff(offline=file_path, prn=lambda x: process_packet(x, packet_data, previous_timestamp))
        
        # Create a DataFrame from the collected packet data
        columns = ['Src_IP', 'Dst_IP', 'Protocol', 'Packet_Size', 'Inter_Arrival_Time', 'Dst_Port', 'Payload_Entropy']
        df = pd.DataFrame(packet_data, columns=columns)

        # Save the DataFrame to a CSV file with the same name as the pcap file
        csv_file_path = os.path.splitext(file_path)[0] + '_processed.csv'
        df.to_csv(csv_file_path, index=False)
