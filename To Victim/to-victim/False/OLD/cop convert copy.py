import csv
from scapy.all import rdpcap, IP, TCP, UDP
import os

def pcap_to_csv(input_pcap, output_csv):
    packets = rdpcap(input_pcap)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Timestamp', 'Source IP', 'Destination IP', 'Protocol', 'Frame Length',
            'Port Used', 'Interpacket Time', 'Entropy'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for i in range(len(packets)):
            current_packet = packets[i]

            timestamp = current_packet.time
            src_ip = current_packet.getlayer(IP).src if 'IP' in current_packet else 'N/A'
            dst_ip = current_packet.getlayer(IP).dst if 'IP' in current_packet else 'N/A'
            protocol = current_packet.getlayer(IP).proto if 'IP' in current_packet else 'N/A'
            frame_length = len(current_packet)
            port_used = current_packet.getlayer(TCP).dport if 'TCP' in current_packet else (current_packet.getlayer(UDP).dport if 'UDP' in current_packet else 'N/A')

            interpacket_time = 0
            if i > 0:
                interpacket_time = timestamp - packets[i - 1].time

            entropy = 0
            if i > 0 and src_ip == packets[i - 1].getlayer(IP).src:
                entropy = timestamp - packets[i - 1].time

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

def process_pcap_folder(input_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pcap"):
            input_pcap_file = os.path.join(input_folder, file_name)
            output_csv_file = os.path.splitext(input_pcap_file)[0] + ".csv"
            pcap_to_csv(input_pcap_file, output_csv_file)

if __name__ == "__main__":
    input_folder = "."  # Replace with your input folder containing .pcap files
    process_pcap_folder(input_folder)
