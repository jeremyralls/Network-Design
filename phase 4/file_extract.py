import math
import struct
import time
# define packet concat array for server
import sys

raw_file_data = bytearray()

# returns the number of packets that need to be sent given a user
# specified packet size
def number_of_packets(fname, packet_size_bytes):
    with open(fname, 'rb') as bmp:
        data = bytearray(bmp.read())
        bmp.close()
        size_of_file = int.from_bytes(data[2:6], "little")
        #print("Size of file: " + str(size_of_file))

        if size_of_file % packet_size_bytes != 0:
            num_of_packets = math.floor(size_of_file/packet_size_bytes) + 1
        else:
            num_of_packets = math.floor(size_of_file/packet_size_bytes)

        return num_of_packets

# ment to run in a for loop were the conditions are based on
# the function "number_of_packets" this returns one buffer of length "packet_size_bytes"

def client_packet_split(packet_size_bytes, fname, i):
    packet_buf = bytearray(0)
    with open(fname, 'rb') as bmp:
        data = bytearray(bmp.read())
        bmp.close()
        packet_buf = data[(packet_size_bytes * i):(packet_size_bytes * (i + 1)) ]

        print("Good: " + str(packet_buf))

        return packet_buf

#takes a packet from the client_packet_split function and switches the first bit of each byte
def client_packet_corruptor(packet_buf):
    for i in packet_buf:
        if bin(packet_buf[i])[len(bin(packet_buf[i])) - 1] == '0':
            packet_buf[i] = packet_buf[i] + 1
        else:
            packet_buf[i] = packet_buf[i] - 1


    print("Corrupt: " + str(packet_buf))

    return packet_buf


# This function will merge the recived packets together and write the bmp file
# for the UDP reciver.  This function will return 1 when the full file
# has been recived to indicate that the loop it is running in can be broken

def server_packet_merge_file_write(rxdata, fname, i, packet_size_bytes):

    raw_file_data[(packet_size_bytes * i):(packet_size_bytes * (i + 1)) ] = rxdata

    with open(fname, 'wb') as bmp:
        bmp.write(raw_file_data)
        bmp.close()

    with open(fname, 'rb') as bmp:
        data = bytearray(bmp.read())
        bmp.close()
        size_of_file = int.from_bytes(data[2:6], "little")

    if(len(raw_file_data) < (size_of_file )):
        return 0
    else:
        return 1

def wraparound(sum,word):
    newsum = sum + word
    fixedsum = (newsum & 0xffff) + (newsum >> 16)

    return fixedsum

def chksum(data):
    sum = 0
    for i in range(0,len(data),2):
        word = data[i] + (data[i+1] << 8)
        sum = wraparound(sum,word)

    return ~sum & 0xffff