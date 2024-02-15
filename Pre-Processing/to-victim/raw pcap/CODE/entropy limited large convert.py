import csv
from scapy.all import PcapReader, IP, TCP, UDP
import os
from tqdm import tqdm

def pcap_to_csv(input_pcap, output_csv, window_size=10):
    with PcapReader(input_pcap) as packets:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Timestamp', 'Source IP', 'Destination IP', 'Protocol', 'Frame Length',
                'Port Used', 'Interpacket Time', 'Entropy'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()

            recent_packets = []  # Store the last N consecutive packets

            for packet in tqdm(packets, desc=f"Processing {os.path.basename(input_pcap)}", unit=" packets"):
                timestamp = packet.time
                src_ip = packet.getlayer(IP).src if 'IP' in packet else 'N/A'
                dst_ip = packet.getlayer(IP).dst if 'IP' in packet else 'N/A'
                protocol = packet.getlayer(IP).proto if 'IP' in packet else 'N/A'
                frame_length = len(packet)
                port_used = packet.getlayer(TCP).dport if 'TCP' in packet else (packet.getlayer(UDP).dport if 'UDP' in packet else 'N/A')

                interpacket_time = 0
                if recent_packets:
                    interpacket_time = timestamp - recent_packets[-1].time

                entropy = 0
                if len(recent_packets) >= window_size and src_ip == recent_packets[-1].getlayer(IP).src:
                    # Calculate entropy based on the last N consecutive packets
                    entropy = timestamp - recent_packets[-window_size].time

                writer.writerow({
                    'Timestamp': timestamp,
                    'Source IP': src_ip,
                    'Destination IP': dst_ip,
                    'Protocol': protocol,
                    'Frame Length': frame_length,
                    'Port Used': port_used,
                    'Interpacket Time': interpacket_time,
                    'Entropy': entropy
                })

                # Maintain the recent packets window
                recent_packets.append(packet)
                if len(recent_packets) > window_size:
                    recent_packets.pop(0)

if __name__ == "__main__":
    input_folder = "."  # Replace with your input folder containing .pcap files
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pcap"):
            input_pcap_file = os.path.join(input_folder, file_name)
            output_csv_file = os.path.splitext(input_pcap_file)[0] + ".csv"
            pcap_to_csv(input_pcap_file, output_csv_file)
