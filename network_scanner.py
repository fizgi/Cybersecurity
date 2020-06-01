#!/usr/bin/python3.8

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]

    return [{"ip": element[1].psrc, "mac": element[1].hwsrc} for element in answered_list]


print(*(x for x in scan("192.168.1.1/24")), sep='\n')
