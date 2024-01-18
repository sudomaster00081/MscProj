import csv
from scapy.all import rdpcap

def pcap_to_csv(input_pcap, output_csv):
    packets = rdpcap(input_pcap)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Timestamp', 'Source IP', 'Destination IP', 'Source MAC', 'Destination MAC',
            'Protocols', 'Packet Length', 'Port', 'IP Protocol', 'Inter-Arrival Time',
            'Payload Data'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for packet in packets:
            timestamp = packet.time
            src_ip = packet.getlayer('IP').src if 'IP' in packet else 'N/A'
            dst_ip = packet.getlayer('IP').dst if 'IP' in packet else 'N/A'
            src_mac = packet.getlayer('Ether').src if 'Ether' in packet else 'N/A'
            dst_mac = packet.getlayer('Ether').dst if 'Ether' in packet else 'N/A'
            protocols = packet.getlayer('IP').payload.name if 'IP' in packet else 'N/A'
            packet_len = len(packet)
            port = packet.getlayer('TCP').dport if 'TCP' in packet else (packet.getlayer('UDP').dport if 'UDP' in packet else 'N/A')
            ip_protocol = packet.getlayer('IP').proto if 'IP' in packet else 'N/A'
            inter_arrival_time = packet.time - timestamp if timestamp else 'N/A'
            payload_data = str(packet.payload) if hasattr(packet, 'payload') else 'N/A'

            writer.writerow({
                'Timestamp': timestamp,
                'Source IP': src_ip,
                'Destination IP': dst_ip,
                'Source MAC': src_mac,
                'Destination MAC': dst_mac,
                'Protocols': protocols,
                'Packet Length': packet_len,
                'Port': port,
                'IP Protocol': ip_protocol,
                'Inter-Arrival Time': inter_arrival_time,
                'Payload Data': payload_data
            })

if __name__ == "__main__":
    input_pcap_file = "ddostrace.to-victim.20070804_134936.pcap"  # Replace with your input pcap file
    output_csv_file = "output.csv"    # Replace with your desired output csv file

    pcap_to_csv(input_pcap_file, output_csv_file)
