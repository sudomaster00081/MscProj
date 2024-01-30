import os
from scapy.all import rdpcap, IP, TCP, UDP
import csv

def extract_features(packet):
    try:
        source_ip = packet.getlayer(IP).src
        destination_ip = packet.getlayer(IP).dst
        protocol = packet.getlayer(IP).proto
        frame_length = len(packet)
        port_used = None

        if 'TCP' in packet:
            port_used = packet[TCP].dport
        elif 'UDP' in packet:
            port_used = packet[UDP].dport

        timestamp = packet.time
        return [source_ip, destination_ip, protocol, frame_length, port_used, timestamp]

    except AttributeError:
        return None  # Ignore packets without IP layer

def main(input_pcap, output_csv):
    packets = rdpcap(input_pcap)
    features_list = []

    for i in range(len(packets)):
        current_packet = packets[i]
        interpacket_time = 0

        if i > 0:
            interpacket_time = current_packet.time - packets[i - 1].time

        features = extract_features(current_packet)

        if features is not None:
            features.append(interpacket_time)

            if i > 0 and features[0] == features_list[-1][0]:
                entropy = current_packet.time - packets[i - 1].time
            else:
                entropy = 0

            features.append(entropy)
            features_list.append(features)

    # Write features to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ["Source IP", "Destination IP", "Protocol", "Frame Length", "Port Used", "Timestamp", "Interpacket Time", "Entropy"]
        csv_writer.writerow(header)
        csv_writer.writerows(features_list)

if __name__ == "__main__":
    input_directory = "."  # Current directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".pcap"):
            input_pcap_file = os.path.join(input_directory, file_name)
            output_csv_file = os.path.splitext(input_pcap_file)[0] + ".csv"
            main(input_pcap_file, output_csv_file)
