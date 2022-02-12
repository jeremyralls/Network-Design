from socket import * #import python socket library
import file_extract

serverPort = 4444
serverSocket = socket(AF_INET, SOCK_DGRAM) #creates server socket
serverSocket.bind(("", serverPort)) #binds socket to server port
print("Ready to receive file from client")

#receive filename from client
filename, clientAddress = serverSocket.recvfrom(2048)
filename = filename.decode()
print("File name: " + filename)

#receive packet size in bytes from client
packet_size_string, clientAddress = serverSocket.recvfrom(2048)
packet_size = int(packet_size_string.decode())
print("Packet size: " + str(packet_size) + " bytes")

#receive all packets from client
i = 0
while True:
    packet, clientAddress = serverSocket.recvfrom(2048) #receives packet from client
    print("Packet " + str(i + 1) + ": " + str(packet))
    new_file = file_extract.server_packet_merge_file_write(packet, (filename + '_copy' + '.bmp'), i, packet_size) #merge packets into a new file
    i += 1