import socket
import sys
import os
import threading
import subprocess
import signal
from DataStructuresManagement import DataStructuresManagement
import Utilities
import Server_functions
import DroneControl
from socket import error as SocketError
import time
import errno


#global constants

HOST='0.0.0.0'
PORT_CONTROL=8888

CLIENT_IPERF_PORT=5201


#global variables

client_running = True

##### END DECLARATION PART #####

#CREATE CONTROL SOCKET TCP

sock_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Control Socket created')

#Bind socket to an address and a port
try:
    sock_control.bind((HOST, PORT_CONTROL))
except socket.error as sock_err_msg:
    print 'Control socket bind failed! Error code: ', sock_err_msg.args[0], "Message",sock_err_msg.args[1]
    print "Exiting..."
    sys.exit()

print 'Control Socket bind complete'

#start listening on Control Socket

sock_control.listen(10)
print 'Control Socket now listening'




def movementthread(id_str,avg):



    movement = Server_functions.cmp_avg_and_decide(id_str,avg)

    DroneControl.execute_movement(movement,1,1)



def streamthread(ip_addr):
    print "Start Iperf3 client"

    global  client_running


    #pipe_name = 'pipe_test'

    #pipeout = os.open(pipe_name, os.O_WRONLY)
    file_temp = open("./file_temp.txt","w")
    process_to_open = 'stdbuf -oL iperf3 -c '+ip_addr+' -u -i 1 -p 5201 -b 0 -t 0'
    p = subprocess.call(process_to_open, shell=True,stdout=file_temp,stderr=file_temp)

    print "THREAD streamthread e' nel loop while true"
    while True:
        time.sleep(1)
    #client_running = False


def clientthread(conn,addr):

    #register client into the data structure
    new_client = (addr[0], addr[1])
    DataStructuresManagement.add_active_clients(new_client)
    print 'Connected with ', addr[0], ':', str(
        addr[1]), "\tactive clients:", DataStructuresManagement.get_active_clients()

    #wait for "ready" client message
    try:

        ready = conn.recv(1024)

    except SocketError as e:
        print "E:SocketError in clientthread: ", e
        Server_functions.close_client_thread(conn,addr)


    iperf_thread = threading.Thread(target=streamthread, args=(addr[0],))
    iperf_thread.start()

    conn.sendall('Welcome to the server\n'.encode())  # send only takes string


    while client_running:

        # Receiving from client
        try:

            data= conn.recv(1024)

        except SocketError as e:
                print "E:SocketError in clientthread: ",e
                break

        '''
        try:
            data = conn.recv(1024)

        except Exception as e:
            print ("ERROR: ",e)
            break
        '''
        if not data:
            break

        data_str=data.decode("utf-8")

        res=Utilities.str_to_i(data_str)

        if res[0] == False:
            print "Not a number, skipped"
            continue

        #DA FARE CON LOGGING
        print "Client %s:%s sent: %s"%(addr[0],addr[1],res[1])

        #Processing data
        id_str = addr[0]+":"+str(addr[1])

        avg=Server_functions.store_value_from_client(id_str,res[1])

        if not avg == -1:
            print "START MOVEMENT_THREAD"
            movement_thread = threading.Thread(target=movementthread, args=(id_str, avg,))
            movement_thread.start()


        reply = b'OK...' + data


        #Sending answer
        conn.sendall(reply)

    DataStructuresManagement.rmv_active_clients((addr[0], addr[1]))


    # came out of loop
    print "CONNECTION CLOSED, address: ", addr,"\tactive clients:", DataStructuresManagement.get_active_clients()


    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = sock_control.accept()


    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

    try:
        proc_thread = threading.Thread(target = clientthread, args=(conn,addr,))
        proc_thread.start()
        #signal.pause()
        #start_new_thread(clientthread, (conn,addr,))
    except (KeyboardInterrupt, SystemExit):
        print '\n! Received keyboard interrupt, quitting threads.\n'


sock_control.close()