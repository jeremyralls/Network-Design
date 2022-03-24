from socket import * #import python socket library
import file_extract
import random

clientName = "localhost"
serverPort = 4444
serverSocket = socket(AF_INET, SOCK_DGRAM) #creates server socket
serverSocket.bind(("", serverPort)) #binds socket to server port
print("Ready to receive file from client")

#receive filename from client
filename, clientAddress = serverSocket.recvfrom(2048)
filename = filename.decode()
print(filename)

#receive packet size in bytes from client
packet_size_string, clientAddress = serverSocket.recvfrom(2048)
packet_size = int(packet_size_string.decode())
print("Packet size: " + str(packet_size) + " bytes")

last_good_packet = '1'

i = 0
while True:
    id, clientAddress = serverSocket.recvfrom(2048) #receive packet ID from client
    id = id.decode()
    ACK = "111" #111 signifies good ACK
    #print("ID " + str(i + 1) + ": " + id)

    checksum, clientAddress = serverSocket.recvfrom(2048) #receive checksum from client
    #print("Checksum " + str(i + 1) + ": " + checksum.decode())

    packet, clientAddress = serverSocket.recvfrom(2048) #receive packet from client
    #print("Packet " + str(i + 1) + ": " + str(packet))

    checksum_calc = file_extract.chksum(packet)
    checksum_calc = str(checksum_calc)
    if checksum.decode() != checksum_calc: #Are the checksums calculated on the client side and server side equal? If not, change ID
        id = last_good_packet #Set the ID to the last good packet
    elif id != last_good_packet: #If the sequence numbers between the current and last packets are the same (unless the last packet was corrupted), don't write the packet to the file
        new_file = file_extract.server_packet_merge_file_write(packet, (filename + '_copy' + '.bmp'), i, packet_size)  # merge packets into a new file
        last_good_packet = id #Record this packet as the last good packet
        i += 1

    if random.randint(0, 100) < 10:  # Corrupt 10% of the ACKs
        ACK = "101"

    response = id + ACK #ACK contains the ID number of the packet sent and 111

    serverSocket.sendto(response.encode(), clientAddress) #Send the ACK back to the client