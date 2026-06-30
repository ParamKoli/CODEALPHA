from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

packet_count = 0

def process_packet(packet):
    global packet_count
    packet_count += 1

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        proto_name = "OTHER"
        if TCP in packet:
            proto_name = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            proto_name = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        else:
            src_port = "N/A"
            dst_port = "N/A"

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"{Fore.CYAN}[{timestamp}] {Fore.GREEN}Packet #{packet_count}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Protocol:{Style.RESET_ALL} {proto_name}")
        print(f"  {Fore.YELLOW}Source IP:{Style.RESET_ALL} {src_ip}:{src_port}")
        print(f"  {Fore.YELLOW}Destination IP:{Style.RESET_ALL} {dst_ip}:{dst_port}")
        print(f"  {Fore.YELLOW}Packet Size:{Style.RESET_ALL} {len(packet)} bytes")

        if packet.haslayer('Raw'):
            payload = bytes(packet['Raw'].load)
            print(f"  {Fore.YELLOW}Payload (first 50 bytes):{Style.RESET_ALL} {payload[:50]}")

        print("-" * 70)

def main():
    print(f"{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}  CodeAlpha - Basic Network Sniffer")
    print(f"{Fore.GREEN}  Param Parag Koli | Cyber Security Internship")
    print(f"{Fore.GREEN}{'='*70}\n")
    print(f"{Fore.CYAN}Starting packet capture... Press Ctrl+C to stop.\n")

    try:
        sniff(prn=process_packet, store=False, count=50)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Sniffer stopped by user.")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        print(f"{Fore.YELLOW}Note: This script requires Administrator/root privileges to capture packets.")

    print(f"\n{Fore.GREEN}Total packets captured: {packet_count}")

if __name__ == "__main__":
    main()