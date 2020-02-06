# -*- coding: utf-8 -*-

from scapy.all import *

def packet_callback(packet):
    print("in callback")
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        
        print(main_packet)
        
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("Server:%s" % packet[IP].dst)
            print("%s" % packet[TCP].payload)
    print(packet.show())
    
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143 or tcp port 993 or tcp port 994 or tcp port 995 or tcp port 465 or tcp port 587 ",prn=packet_callback,store=0)