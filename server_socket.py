import socket
import sys
import threading
from DataStructuresManagement import DataStructuresManagement
import Utilities
import Server_functions
import DroneControl

HOST='0.0.0.0'
PORT=8888



#CREATE SOCKET

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('socket created')

#Bind socket to an address and a port
try:
    sock.bind((HOST, PORT))
except socket.error as sock_err_msg:
    print ('Bind failed!!! Error code: ', sock_err_msg.args[0], "Message",sock_err_msg.args[1])
    print("Exiting...")
    sys.exit()

print ('Socket bind complete')

#start listening on socket

sock.listen(10)
print ('Socket now listening')


def movementthread(id_str,avg):



    movement = Server_functions.cmp_avg_and_decide(id_str,avg)

    DroneControl.execute_movement(movement,1,1)






def clientthread(conn,addr):
    # Sending message to connected client
    conn.send('Welcome to the server\n'.encode())  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.


    while True:

        # Receiving from client
        try:
            data = conn.recv(1024)

        except ConnectionResetError:
            break

        if not data:
            break

        data_str=data.decode("utf-8")

        res=Utilities.str_to_i(data_str)

        if res[0] == False:
            print("Not a number, skipped")
            continue

        #DA FARE CON LOGGING
        print("Client %s:%s sent: %s"%(addr[0],addr[1],res[1]))

        #Processing data
        id_str = addr[0]+":"+str(addr[1])

        avg=Server_functions.store_value_from_client(id_str,res[1])

        if not avg == -1:
            print("START MOVEMENT_THREAD")
            movement_thread = threading.Thread(target=movementthread, args=(id_str, avg,))
            movement_thread.start()


        ######DAFAREEEEE



        reply = b'OK...' + data


        #Sending answer
        conn.sendall(reply)

    DataStructuresManagement.rmv_active_clients((addr[0], addr[1]))


    # came out of loop
    print("CONNECTION CLOSED, address: ", addr,"\tactive clients:", DataStructuresManagement.get_active_clients())


    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = sock.accept()

    new_client = (addr[0],addr[1])
    DataStructuresManagement.add_active_clients(new_client)
    print('Connected with ', addr[0], ':', str(addr[1]),"\tactive clients:", DataStructuresManagement.get_active_clients())

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

    proc_thread = threading.Thread(target = clientthread, args=(conn,addr,))
    proc_thread.start()
    #start_new_thread(clientthread, (conn,addr,))

sock.close()