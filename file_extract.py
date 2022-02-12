import math
# define packet concat array for server
raw_file_data = bytearray()

# returns the number of packets that need to be sent given a user
# specified packet size
def number_of_packets(fname, packet_size_bytes):
    with open(fname, 'rb') as bmp:
        data = bytearray(bmp.read())
        bmp.close()
        size_of_file = int.from_bytes(data[2:6], "little")

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
