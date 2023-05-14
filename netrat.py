#!/usr/bin/env python
from scapy import *
import sys
import os
import subprocess
import threading
import socket
import re
import colorama
import argparse as arg
#importing necesssery libraries that NetRat needs to work properly.

#ip adress signature
ip = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

def needhelp():
    print("""NEEDHELP = active""")

def mitm():
    

def portus():

    arguments = arg.ArgumentParser()
    arguments.add_argument('mode', type=str)
    arguments.add_argument('time', type=int)
    arguments.add_argument('ipadress', type=int)
    arguments.add_argument('portmin', type=int)
    arguments.add_argument('portmax', type=int)
    add_help=False
    arr = arguments.parse_args(sys.argv[2:])

    if arr.mode == "-q":
        for x in range(arr.portmin,arr.portmax):
            srvs = socket.getservbyport(x)
            ip = IP(dst=arr.ipadrress)
            tcp = TCP(sport=RandShort(), dport=arr.ipadress, flags="S", seq=RandInt(), options=[('MSS', 1460)])
            syn_packet = ip/tcp
            response = sr(syn_packet, verbose=0)
            if response:
                tcp_response = response[0][1]
                if tcp_response.haslayer(TCP) and tcp_response[TCP].flags == "SA":
                    print(f"[*] {x} is opened: {srvs} ")
            



    elif arr.mode == "-c":
        for x in range(arr.portmin,arr.portmax):
            srvs = socket.getservbyport(x)
            connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket.setdefaulttimeout(arr.time)
            rs = connection.connect_ex((arr.ipadress,x))
            if rs and rs == 0:
                print(f"[*] {x} is opened: {srvs} ")
    
    else:
        sys.exit("invalid arguments!")






try:
    arg1 = sys.argv[1]

except IndexError:
    sys.exit()
    #made by MARTIN RAJNOCH
