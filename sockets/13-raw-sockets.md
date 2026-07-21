# Part 13: Raw Sockets & Packet Capture (Demystified)

## Why Does This Matter?
Up until now, you've used standard TCP (`SOCK_STREAM`) and UDP (`SOCK_DGRAM`) sockets. With these, the Operating System does all the heavy lifting. You hand the OS a message, and it adds the TCP/UDP headers, the IP headers, the Ethernet headers, and sends it out. When you receive data, the OS strips away all those headers and just hands you the pure payload.

But what if you want to build a tool like `ping`, `traceroute`, `tcpdump`, or `Wireshark`? What if you want to craft an entirely custom protocol that doesn't use TCP or UDP? What if you want to inspect **every single packet** flowing across your Wi-Fi card, including those meant for other people?

To do that, you need to bypass the OS's hand-holding. You need a **Raw Socket**.

---

## The Real-World Analogy: The Telephone vs. The Wiretap

📞 **Normal Sockets (TCP/UDP):** It's like using a telephone. You dial a number, say "Hello," and the phone company handles routing your voice, establishing the connection, and handling interference. You only care about the conversation.

✂️ **Raw Sockets:** It's like climbing a telephone pole, stripping the insulation off the main wire, and hooking up alligator clips directly to the copper. You don't just hear your own conversation—you hear the raw electrical signals of *everyone's* conversations. You have to decode the beeps and boops yourself. And if you inject your own electrical signals, you can forge caller IDs (spoofing) or break the whole system.

Because raw sockets are so powerful (like tapping a phone wire), they come with a huge restriction: **You must be `root` (Administrator) to use them.**

---

## Security Implications: Why Do We Need Root?

⚠️ **WARNING:** Most of the code in this chapter **will crash with a `PermissionError`** unless you run it with `sudo` (Linux/macOS) or as Administrator (Windows).

Why? 
1. **Eavesdropping (Packet Sniffing):** You can read passwords, cookies, and emails sent by other users on your machine or network.
2. **Spoofing:** You can forge the "Source IP" in the IP header, making it look like your packet came from Google or your bank.
3. **Denial of Service:** You can easily flood a network with malformed, hand-crafted packets designed to crash routers.

Because of this, modern operating systems tightly restrict raw socket access. Linux requires `root` (or the `CAP_NET_RAW` capability). Windows has even restricted what raw sockets can do (more on that later).

---

## 1. `SOCK_RAW` over `AF_INET`: Playing with IP Packets

When you create a raw socket using the `AF_INET` family (IPv4), you are telling the OS:
*"Do not strip the IP header. Give me the whole IP packet. If I send data, I will build the inner protocol (like ICMP or TCP) myself."*

### IP Packet Structure

When you read from an `AF_INET` raw socket, the data you get starts exactly here:

```text
       IPv4 Header (Usually 20 bytes)
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Payload (e.g. TCP/UDP/ICMP...)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### TCP Segment Structure (The Payload)

If the `Protocol` field in the IP header is `6`, the payload is a TCP segment:

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Example: Building a Ping Tool (ICMP)

The `ping` command does not use TCP or UDP. It uses ICMP (Internet Control Message Protocol, Protocol `1`). To send an ICMP Echo Request, we *have* to use a raw socket.

```python
import socket
import struct
import os
import time

# Checksum calculation function needed for ICMP headers
def checksum(source_string):
    sum = 0
    max_count = (len(source_string) // 2) * 2
    count = 0
    while count < max_count:
        val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + val
        sum = sum & 0xffffffff
        count = count + 2
    if max_count < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# 1. Create a raw socket for ICMP
# Requires root! (e.g., sudo python3 ping.py)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except PermissionError:
    print("Run this script as root! (sudo)")
    exit(1)

# 2. Build the ICMP Header (Type=8 for Echo Request, Code=0)
# format: type (B), code (B), checksum (H), id (H), sequence (H)
header = struct.pack("bbHHh", 8, 0, 0, os.getpid() & 0xFFFF, 1)
data = b"hello_world_ping" # Arbitrary payload

# Calculate the checksum on the header + data
my_checksum = checksum(header + data)

# Rebuild the header with the correct checksum
header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), os.getpid() & 0xFFFF, 1)
packet = header + data

# 3. Send the packet directly to a destination
dest_ip = socket.gethostbyname("google.com")
print(f"Pinging {dest_ip}...")
s.sendto(packet, (dest_ip, 1)) # Port number doesn't matter for ICMP

# 4. Receive the reply
# The OS gives us the ENTIRE IP packet, starting from the IP header
recv_packet, addr = s.recvfrom(65535)
print(f"Received reply from {addr[0]}: {len(recv_packet)} bytes")

# The first 20 bytes are the IP header, the ICMP reply starts at byte 20!
icmp_header = recv_packet[20:28]
type, code, chksum, p_id, seq = struct.unpack("bbHHh", icmp_header)

if type == 0: # Type 0 = Echo Reply
    print(f"Success! ICMP Echo Reply (Sequence: {seq})")
```

### `IP_HDRINCL`: Total Control

In the example above, we built the ICMP header, but the OS still built the IP header for us. 
If we want to build the IP header manually (e.g., to spoof the source IP address), we set the `IP_HDRINCL` option:

```python
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# Now s.sendto() expects you to provide the IP header AND the payload!
```

---

## 2. `AF_PACKET` on Linux: Raw Ethernet Frames

`SOCK_RAW` with `AF_INET` operates at Layer 3 (Network Layer - IP packets).
But what if we want to go lower? What if we want to see MAC addresses? What if we want to intercept ARP requests or build our own Wi-Fi deauthentication frames?

On Linux, we use `AF_PACKET`. This gives us Layer 2 (Data Link Layer - Ethernet frames).

### Ethernet Frame Structure

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Destination MAC Address (6 bytes)       | Source MAC... |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       ...Source MAC Address (6 bytes)         |   EtherType   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                      Payload (46 - 1500 bytes)                |
|               (usually an IP packet or ARP packet)            |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Frame Check Sequence (FCS)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Building a Mini Packet Sniffer (Linux Only)

This code captures every single Ethernet frame passing through your network card. This is exactly how `tcpdump` works.

```python
import socket
import struct
import binascii

# ETH_P_ALL is 0x0003 in C, but we must use ntohs to fix byte order
ETH_P_ALL = socket.ntohs(0x0003)

try:
    # AF_PACKET gives us raw ethernet frames (Linux only)
    sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, ETH_P_ALL)
except AttributeError:
    print("AF_PACKET is Linux only!")
    exit(1)
except PermissionError:
    print("Need root privileges to sniff packets!")
    exit(1)

# Bind to a specific interface (optional, usually "eth0" or "wlan0")
# sniffer.bind(("eth0", 0))

print("Listening for packets...")
while True:
    # 65535 is the max size of a packet
    raw_data, addr = sniffer.recvfrom(65535)
    
    # Extract the first 14 bytes (Ethernet Header)
    eth_length = 14
    eth_header = raw_data[:eth_length]
    
    # Unpack the MAC addresses and EtherType
    # 6s = 6 bytes (string), H = 2 bytes (unsigned short)
    eth = struct.unpack('!6s6sH', eth_header)
    
    # Format MAC addresses to human readable hex
    dest_mac = binascii.hexlify(eth[0]).decode().upper()
    src_mac = binascii.hexlify(eth[1]).decode().upper()
    eth_proto = hex(eth[2])
    
    # Format e.g., 001122334455 -> 00:11:22:33:44:55
    def format_mac(mac):
        return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
        
    print(f"\nEthernet Frame:")
    print(f"  Destination: {format_mac(dest_mac)}")
    print(f"  Source:      {format_mac(src_mac)}")
    print(f"  Protocol:    {eth_proto}")
    
    if eth_proto == '0x800': # 0x0800 means the payload is an IPv4 packet!
        print("  Payload is IPv4!")
```

---

## 3. Windows Raw Sockets (The Limitations)

Windows used to be an attacker's dream, but Microsoft cracked down on raw sockets in Windows XP SP2 to stop malware from easily spoofing IP addresses.

On modern Windows:
- `AF_PACKET` does not exist. You cannot easily read raw Ethernet frames using standard Python sockets.
- You **cannot** send raw TCP packets (`IPPROTO_TCP` over raw sockets is blocked).
- You **can** sniff packets in "promiscuous mode" using a special `ioctl` call, but it's limited to IP packets (`AF_INET`), not Ethernet frames.

### Sniffing on Windows (`SIO_RCVALL`)

```python
import socket
import os

HOST = socket.gethostbyname(socket.gethostname())

# Create raw socket (must run as Admin)
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Tell the OS to include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Turn on promiscuous mode (SIO_RCVALL) - Windows ONLY
# RCVALL_ON is 1. ioctl cmd is 0x98000001
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

print(f"Sniffing on {HOST}...")
print(s.recvfrom(65535))

# Turn off promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
```

---

## 4. Scapy: How Professionals Do It

Crafting raw bytes with `struct.pack()` is a great academic exercise to learn how networking actually works under the hood. 

However, in the real world, **nobody writes networking tools in Python using raw sockets by hand.** The checksum math, endianness, bit-shifting, and parsing logic is too error-prone and tedious.

Instead, professionals use a library called **Scapy**.

Scapy is a powerful Python library built on top of raw sockets (and `libpcap` / `Npcap`) that makes building and parsing packets ridiculously easy.

### Building an ICMP Ping in Scapy (One Line)

Compare this to the huge block of `struct` math we did earlier:

```python
from scapy.all import IP, ICMP, sr1

# Build an IP layer, stack an ICMP layer on top of it, and send it
packet = IP(dst="8.8.8.8") / ICMP()
reply = sr1(packet, timeout=2)

print(reply.summary())
```

### Building an ARP Scanner Concept

To discover all devices on your local network, you can broadcast an ARP request asking "Who has IP 192.168.1.X?". With Scapy, it's trivial:

```python
from scapy.all import Ether, ARP, srp

# Broadcast MAC / ARP Request for a whole subnet
packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24")

# Send and receive (srp)
answered, unanswered = srp(packet, timeout=2, verbose=0)

print("Devices on network:")
for sent, received in answered:
    print(f"IP: {received.psrc}  MAC: {received.hwsrc}")
```

---

## 5. Packet Capture vs. Packet Injection

It's important to understand the two sides of raw sockets:

1. **Packet Capture (Sniffing):** Passively reading packets off the wire. This is what Wireshark does. On a switched network, you normally only see traffic destined for your MAC address, plus broadcasts. To see *everyone's* traffic (like on open Wi-Fi), you must put your network card into **Promiscuous Mode** (Monitor Mode for Wi-Fi).
2. **Packet Injection:** Actively creating and sending malformed or spoofed packets onto the network. This is what tools like `nmap` and `hping3` do. 

---

## 6. Security and Ethical Considerations

🛑 **A Critical Warning:**

The ability to craft arbitrary packets and sniff network traffic is the foundation of network security and hacking. 
- You can scan ports bypassing OS firewalls.
- You can spoof ARP replies to perform Man-in-the-Middle (MitM) attacks.
- You can forge source IPs.

**NEVER use raw sockets to scan, sniff, or attack networks, machines, or servers that you do not personally own or do not have explicit, written permission to test.**

Doing so on a corporate network, a university network, or the public internet is considered malicious activity and is often illegal. Keep your experiments on `localhost` (`127.0.0.1`) or a private home lab.

---

## Quick Reference Summary

| Concept | Explanation | Platform |
|---------|-------------|----------|
| `AF_INET` + `SOCK_RAW` | Raw IP packets. You provide the transport layer (TCP/UDP/ICMP). OS provides IP header (unless `IP_HDRINCL`). | Linux/macOS/Windows |
| `IPPROTO_ICMP` | Used to capture/send ICMP (ping) packets specifically. | Cross-platform |
| `IP_HDRINCL` | Tells the OS "Don't add the IP header, I am providing it." | Cross-platform |
| `AF_PACKET` | Raw Ethernet frames (Layer 2). You provide MAC addresses. | **Linux ONLY** |
| `SIO_RCVALL` | Promiscuous mode IOCTL for sniffing IP traffic. | **Windows ONLY** |
| `Scapy` | Third-party Python library to avoid doing all of this by hand. | Cross-platform |

---

## Self-Check Questions

1. Why does running a raw socket Python script usually result in a `PermissionError`?
2. If you read from an `AF_INET` `SOCK_RAW` socket, what is the very first byte of data you receive?
3. What is the difference between `AF_INET` (Layer 3) raw sockets and `AF_PACKET` (Layer 2) raw sockets?
4. Why is Windows generally a poor environment for writing custom raw packet injection tools?
5. True or False: You should always construct TCP headers manually using `struct` in production applications.

[Back to Main Notes](Notes.md)
