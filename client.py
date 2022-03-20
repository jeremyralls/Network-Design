from socket import * #import python socket library
import file_extract
from tkinter import *
from tkinter.ttk import Progressbar

#send all packets to server
def go():

    BMP_fname = file.get()              #get file name from user input
    packet_size_bytes = 1024            #fixed packet size

    loop_cond = file_extract.number_of_packets((BMP_fname + '.bmp'), packet_size_bytes)  # determine loop conditions before sending packets

    clientSocket.sendto(BMP_fname.encode(), (serverName, serverPort))  # send file name to server

    # send packet size in bytes to server
    val = str(packet_size_bytes)
    clientSocket.sendto(val.encode(), (serverName, serverPort))

    down = Label(                   #making "uploading" text box when button pressed
        gui,
        text='Uploading',
        bg= "grey" ,
        fg="white"
    )
    down.place(x=65, y=220)         #putting it to GUI

    id = "0" #sequence ID starts at 0

    i = 0 #iterator for what packet to send
    j = 0 #iterator for determining which packets will be corrupted
    while i < loop_cond:
        flag = True
        while flag:
            clientSocket.sendto(id.encode(), (serverName, serverPort)) #send sequence ID

            packet_for_tx = file_extract.client_packet_split(packet_size_bytes, BMP_fname + '.bmp', i) #parse file into packets

            if j % 5 == 0: #Corrupt every 5 packets
                checksum = "1" #CHANGE THIS. IMPLEMENT REAL CHECKSUM
                packet_for_tx = file_extract.client_packet_corruptor(packet_for_tx)
            else:
                checksum = "0" #CHANGE THIS. IMPLEMENT REAL CHECKSUM

            clientSocket.sendto(checksum.encode(), (serverName, serverPort)) #send checksum

            clientSocket.sendto(packet_for_tx, (serverName, serverPort)) #send packet

            response, serverAddress = clientSocket.recvfrom(2048) #receive ACK from server
            response = response.decode()
            print("Response: " + response)

            if response[0] == id and response[1:4] == "111": #if neither of the two scenarios below occur, exit the loop. We don't need to send the packet again
                flag = False
            elif response[1:4] == "101": #if the ACK is corrupted, send the packet again
                print("Sending again because of corrupted ACK")
            else: #if the packet was corrupted, send the packet again
                print("Sending again because of corrupted packet")
            j += 1

        if id == "0": #Toggle the sequence number for every packet
            id = "1"
        else:
            id = "0"

        i += 1

        gui.update_idletasks()              #update % in GUI
        pb['value'] += 100 / loop_cond
        txt['text'] = pb['value'], '%'

    down.config(text="Sent")            #changing text from "uploading" to "done"
    txt.config(text= "100%")            #fixes 99.9999% bug instead of 100%


gui = Tk()          #acess tkinter GUi easier
ent = Entry(gui)

gui.title('socket')         #title of popup
gui.geometry('200x300')     #size of popup
gui.config(bg='#345')       #background color of popup


name = Label(               #lable for box where file name in inputed
    gui,
    text = 'Input file name',
    bg = '#345',
    fg = "white"
)

name.place(x=50, y=15)      #placing it on the GUI

file = Entry(gui)           #text box for file name
file.place(x=30, y=40)      #placing on GUI

pb = Progressbar(           #making progress bar
    gui,
    orient = HORIZONTAL,
    length = 100,
    mode = 'determinate'
    )

pb.place(x=40, y=150)           #placing on GUI

txt = Label(                #making progress % on gui
    gui,
    text = '0%',
    bg = '#345',
    fg = "white"

)

txt.place(x=150 ,y=150 )    #placing progess %


button = Button(                     #making button for user to send
    gui,
    text='Send',
    command=go              #function code will go when button pressed

)

button.place(x=75, y=180)   #placing on GUI

serverName = "localhost" #host is local to machine
serverPort = 4444
clientSocket = socket(AF_INET, SOCK_DGRAM) #creates client socket


gui.mainloop()

clientSocket.close() #closes port