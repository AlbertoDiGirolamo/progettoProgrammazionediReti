# -*- coding: utf-8 -*-
"""
GATEWAY
"""

import socket
import time

server = (("localhost", 9100))

buffer_size = 128

n_device = 4
gateway_UDP_port = 9000

gateway_ip_device_interface = "192.168.1.1"
gateway_ip_server_interface = "10.10.10.1"
gateway_mac = "30:05:0A:EF:12:10"

server_ip = "10.10.10.1"
server_mac = "00:00:0A:BB:12:11"

gateway_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_UDP.bind(("localhost", gateway_UDP_port))

devices_ip = []
devices_data = []
arp_table = []
while True:
    
    try:
        print('\n\r waiting to devices connection...')
        message = ''
          
        while(len(devices_ip) < n_device):
            data, address = gateway_UDP.recvfrom(buffer_size)
            data = data.decode('utf8')
            source_mac = data[0: 17]
            source_ip  = data[34: 45]
            source_port = data[56 : 61]
            device_data = data[66:]
            
            UDP_header = str(gateway_UDP_port).zfill(5) + str(source_port).zfill(5)
            header_mac = gateway_mac + source_mac
            header_ip = gateway_ip_device_interface + source_ip                
            
            if (source_ip not in devices_ip):
                response_packet = header_mac + header_ip + UDP_header + 'Packet received..\n'
                gateway_UDP.sendto(bytes(response_packet,"utf-8"), ('localhost', int(source_port)))
                devices_ip.append(source_ip)
                devices_data.append(device_data)
                print(source_ip + ' connected\n')
        
        gateway_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gateway_TCP.connect(server)
        gateway_TCP_port = str(gateway_TCP.getsockname()[1])
        
        TCP_header = str(gateway_TCP_port).zfill(5) + str(source_port).zfill(5)
        header_ip  = gateway_ip_server_interface + server_ip
        header_mac = gateway_mac + server_mac      
        message = header_mac + header_ip + TCP_header
        
        for i in range(n_device):
            message += devices_data[i]

        start = time.time()

        gateway_TCP.sendto(bytes(message, "utf-8"), server)
        response = gateway_TCP.recv(buffer_size)
        response = response.decode("utf-8")
        
        end = time.time()
        print(response[65:] +"\nTCP Trasmission time: ", end-start, " s.\n")
        print('Size buffer of TCP and UDP trasmissions is: ', buffer_size, '\n')
        gateway_TCP.close()
        devices_ip.clear()
        devices_data.clear()

    except IOError:
        gateway_UDP.close()
        gateway_TCP.close()
    
    
    