from socket import * #import python socket library
import file_extract

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

last_id = 1
last_packet_corrupted = False

i = 0
while True:
    id, clientAddress = serverSocket.recvfrom(2048) #receive packet ID from client
    id = id.decode()
    ACK = "111" #111 signifies good ACK
    print("ID " + str(i + 1) + ": " + id)

    checksum, clientAddress = serverSocket.recvfrom(2048) #receive checksum from client
    print("Checksum " + str(i + 1) + ": " + checksum.decode())

    packet, clientAddress = serverSocket.recvfrom(2048) #receive packet from client
    print("Packet " + str(i + 1) + ": " + str(packet))

    temp = False
    checksum_calc = "0" #CHANGE THIS. THIS SHOULD BE THE CHECKSUM CALCULATION ON THE SERVER SIDE
    if checksum.decode() != checksum_calc: #Are the checksums calculated on the client side and server side equal? If not, change ID
        temp = True
        if id == "0":
            id = "1"
        else:
            id = "0"
    elif id != last_id or last_packet_corrupted: #If the sequence numbers between the current and last packets are the same (unless the last packet was corrupted), don't write the packet to the file
        new_file = file_extract.server_packet_merge_file_write(packet, (filename + '_copy' + '.bmp'), i, packet_size)  # merge packets into a new file
        if (i + 3) % 25 == 0: #Corrupt the packet for every few packets
            ACK = "101" #Assume that the last three bits of the ACK must be 111 or else the packet is corrupted
        i += 1

    last_packet_corrupted = temp #Record if the last packet was corrupted

    last_id = id #Record the last ID to ensure that we don't record packets of the same ID in a row

    response = id + ACK #ACK contains the ID number of the packet sent and 111

    serverSocket.sendto(response.encode(), clientAddress) #Send the ACK back to the client