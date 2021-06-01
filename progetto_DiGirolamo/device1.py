# -*- coding: utf-8 -*-
"""
DEVICE 1
"""

import socket
import time
import datetime
import random as rn

def random_time(i):    
    date = datetime.datetime.now()    
    return f"{date.hour}:{date.minute}:{date.second}"
def random_temperature():
    t = rn.randint(20, 35) 
    return f"{t}°C"
def random_humidity():
    u = rn.randint(25, 40)
    return f"{u}%"

buffer_size = 128

device1_ip = "192.168.1.2"
device1_mac = "31:05:0B:EF:19:01"

gateway_ip = "192.168.1.1"
gateway_mac = "30:05:0A:EF:12:10"

header_ip  = device1_ip + gateway_ip 
header_mac = device1_mac + gateway_mac 

gateway_port = 9000
gateway = ("localhost",gateway_port)

number_measurements = 2

while True:
    try:
        message = ''
        for i in range(number_measurements):
            time.sleep(24/number_measurements)      
            msg = f"{device1_ip}-{random_time(i)}-{random_temperature()}-{random_humidity()}\n"
            message += msg
            print(msg)      
            
        device1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        device1.connect(gateway)
        device1_port = str(device1.getsockname()[1])
        UDP_header = str(device1_port).zfill(5) + str(gateway_port).zfill(5)
        message = header_mac + header_ip + UDP_header + message

        start = time.time()
        device1.sendto(message.encode(),gateway)
        response, address = device1.recvfrom(buffer_size)
        response = response.decode("utf-8")
        
        end = time.time()
        
        print(response[66:] +"\nUDP trasmission time: ", end-start, " s.\n")
        print('Size buffer of UDP trasmission is ', buffer_size, '\n')
        device1.close()
    except IOError:
        device1.close()
    