# -*- coding: utf-8 -*-
"""
SERVER TCP
"""

import socket

buffer_size = 512
server_ip = "10.10.10.1"
server_mac = "00:00:0A:BB:12:11"
server_port = 9100

server_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost',server_port)
server_TCP.bind(server_address)
server_TCP.listen(1)

print('The Server is up on port: ',server_port)

while True:    
    try:    
        print ('Ready to serve...')
        connectionSocket, addr = server_TCP.accept()
        
        message = connectionSocket.recv(buffer_size)
        message = message.decode("utf-8")
        
        source_mac = message[0:17]
        source_ip = message[34:45]
        source_port = message[54 : 59]
        message = message[64 :]
        
        print('Size buffer of TCP transmission: ', buffer_size, '\n')
        print(message)
        
        header_mac = server_mac + source_mac
        header_ip  = server_ip  + source_ip
        TCP_header =  str(server_port).zfill(5) + str(source_port).zfill(5)
        
        responce_packet = header_mac + header_ip + TCP_header + 'Packet received..\n'
        connectionSocket.send(bytes(responce_packet, 'utf-8'))

    except IOError:
        connectionSocket.close()