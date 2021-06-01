# -*- coding: utf-8 -*-
"""
DEVICE 3
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

device3_ip = "192.168.1.4"
device3_mac = "31:05:0B:EF:19:03"

gateway_ip = "192.168.1.1"
gateway_mac = "30:05:0A:EF:12:10"

header_ip  = device3_ip + gateway_ip 
header_mac = device3_mac + gateway_mac 

gateway_port = 9000
gateway = ("localhost",gateway_port)

number_measurements = 2

while True:
    try:
        message = ''       
        for i in range(number_measurements):
            time.sleep(24/number_measurements) 
            msg = f"{device3_ip}-{random_time(i)}-{random_temperature()}-{random_humidity()}\n"
            message += msg
            print(msg)
                
        device3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        device3.connect(gateway)   
        device3_port = str(device3.getsockname()[1])
        UDP_header = str(device3_port).zfill(5) + str(gateway_port).zfill(5)
        message = header_mac + header_ip + UDP_header + message

        start = time.time()
        device3.sendto(message.encode(),gateway)
        response, address = device3.recvfrom(buffer_size)
        response = response.decode("utf-8")
        
        end = time.time()
        
        print(response[66:] +"\nUDP trasmission time: ", end-start, " s.\n")
        print('Size buffer of UDP trasmission is ', buffer_size, '\n')
        device3.close()
    except IOError:
        device3.close()