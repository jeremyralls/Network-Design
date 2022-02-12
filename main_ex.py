import file_extract

packet_size_bytes = 200; # arbitrary number selected
# number must be less that UDP max packet size
BMP_fname = 'takis'


# determine loop conditions before sending packets
loop_cond = file_extract.number_of_packets((BMP_fname + '.bmp'), packet_size_bytes);
# Test File Parse full system pass through
exit_condition = 0;
x = 0;
while (exit_condition == 0):
    # client end host 0 =======================================================
    ## use the loop condition from the "number_of_packets" function to exit
    ## know when to exit the send loop
    packet_for_tx = file_extract.client_packet_split(packet_size_bytes, 'takis.bmp', x)
    x = x + 1;
    #Transmit data here
    # Socket.sendto(packet_for_tx, ("127.0.0.1",7070));
    packet_for_rx = packet_for_tx
    # server end host 1 =======================================================
    #Socket.recvfrm(packet_for_tx, ("127.0.0.1",7070));
    # check validity of data here
    # pretend this function is running on a diffrent host
    exit_condition = file_extract.server_packet_merge_file_write(packet_for_rx,(BMP_fname + '_copy'+'.bmp'), x, packet_size_bytes)
    ## this function expects that allo data is correct before input
    print(exit_condition);
