# 🔍 Basic Network Sniffer

**Name:** Param Parag Koli
**Internship:** CodeAlpha — Cyber Security
**Task:** Task 1

## Objective
Build a Python program to capture network traffic packets, analyze their structure and content, and understand how data flows through the network.

## Files
| File | Description |
|------|-------------|
| `sniffer.py` | Main Python script for packet capturing |
| `sniffer_output.txt` | Sample output showing 50 captured packets |

## Tech Stack
Python, Scapy, Colorama

## Features
- Captures live network packets using Scapy
- Displays source and destination IP addresses
- Identifies protocol (TCP/UDP)
- Shows source and destination ports
- Displays packet size and payload preview
- Color-coded terminal output for readability
- Captures 50 packets per run

## How to Run

1. Install dependencies:
```bash
pip install scapy colorama
```

2. Install Npcap (required for Windows packet capture): https://npcap.com

3. Run as Administrator:
```bash
python sniffer.py
```

## Note
This script requires Administrator/root privileges to capture network packets since it accesses the network interface at a low level.
