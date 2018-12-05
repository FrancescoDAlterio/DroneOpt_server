import socket
import sys
import threading
import signal
from DataStructuresManagement import DataStructuresManagement
import Utilities
import Server_functions
import DroneControl
from socket import error as SocketError
import errno

HOST='0.0.0.0'
PORT_CONTROL=8888
PORT_STREAM=9999

#CREATE STREAM SOCKET

sock_stream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ('Stream Socket created')

#Bind stream socket to an address and a port
try:
    sock_stream.bind((HOST, PORT_STREAM))
except socket.error as sock_err_msg:
    print 'Stream socket bind failed! Error code: ', sock_err_msg.args[0], "Message",sock_err_msg.args[1]
    print "Exiting..."
    sys.exit()

print 'Stream Socket bind complete'

#CREATE CONTROL SOCKET

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






def clientthread(conn,addr):
    # Sending message to connected client

    # infinite loop so that function do not terminate and thread do not end.

    cl_udp_port = Server_functions.wait_for_udp_port_num(conn)

    if cl_udp_port == -1:
        print "closing connection"
        conn.close()
        return

    new_client = (addr[0], addr[1], cl_udp_port)
    DataStructuresManagement.add_active_clients(new_client)
    print 'Connected with ', addr[0], ':', str(
        addr[1]),"udp port:",cl_udp_port, "\tactive clients:", DataStructuresManagement.get_active_clients()

    conn.sendall('Welcome to the server\n'.encode())  # send only takes string


    while True:

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

    DataStructuresManagement.rmv_active_clients((addr[0], addr[1],cl_udp_port))


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