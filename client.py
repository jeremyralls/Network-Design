from socket import * #import python socket library
import file_extract

packet_size_bytes = 200 #arbitrary size for each packet in bytes
#number must be less that UDP max packet size
BMP_fname = 'takis' #file name

serverName = "localhost" #host is local to machine
serverPort = 4444
clientSocket = socket(AF_INET, SOCK_DGRAM) #creates client socket

loop_cond = file_extract.number_of_packets((BMP_fname + '.bmp'), packet_size_bytes) #determine loop conditions before sending packets

clientSocket.sendto(BMP_fname.encode(), (serverName, serverPort)) #send file name to server

#send packet size in bytes to server
val = str(packet_size_bytes)
clientSocket.sendto(val.encode(), (serverName, serverPort))

#send all packets to server
i = 0
while i < loop_cond:
    packet_for_tx = file_extract.client_packet_split(packet_size_bytes, 'takis.bmp', i) #parse file into packets
    clientSocket.sendto(packet_for_tx, (serverName, serverPort)) #send packets
    i += 1

clientSocket.close() #closes port
