from scapy.all import *
import pandas as pd
import os
from math import log2

# Function to calculate entropy
def calculate_entropy(data):
    entropy = 0
    total_count = len(data)
    value_counts = data.value_counts()
    for count in value_counts:
        probability = count / total_count
        entropy -= probability * log2(probability)
    return entropy

# Function to extract features from pcap file
def extract_features_from_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    
    # Initialize lists to store extracted features
    src_ips = []
    src_ports = []
    dst_ports = []
    packet_protocols = []
    total_packets = len(packets)
    
    # Extract features from each packet
    for packet in packets:
        if IP in packet:
            src_ips.append(packet[IP].src)
            if packet.haslayer(TCP) or packet.haslayer(UDP):
                src_ports.append(packet[IP].sport)
                dst_ports.append(packet[IP].dport)
            else:
                src_ports.append(None)
                dst_ports.append(None)
            packet_protocols.append(packet[IP].proto)
    
    # Calculate entropies
    etpSrcIP = calculate_entropy(pd.Series(src_ips))
    etpSrcP = calculate_entropy(pd.Series(src_ports))
    etpDstP = calculate_entropy(pd.Series(dst_ports))
    etpProtocol = calculate_entropy(pd.Series(packet_protocols))
    
    return {
        'etpSrcIP': etpSrcIP,
        'etpSrcP': etpSrcP,
        'etpDstP': etpDstP,
        'etpProtocol': etpProtocol,
        'totalPacket': total_packets
    }

# Iterate over pcap files in the directory
pcap_files = [file for file in os.listdir() if file.endswith('.pcap')]
for pcap_file in pcap_files:
    print(f'Processing {pcap_file}...')
    features = extract_features_from_pcap(pcap_file)
    filename = os.path.splitext(pcap_file)[0] + '.csv'
    pd.DataFrame([features]).to_csv(filename, index=False)
    print(f'Features extracted and saved to {filename}')
