
import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5500  # socket server port number

    filedata = ""
    with open("users.txt", "r", errors='ignore') as file:
       for line in file:
          line = line.strip('\n')
          filedata+=line+" "


    file = filedata.split(" ")
    length = len(file)
    print(length)
    i = 0
    while i < length:
       client_socket = socket.socket()  # instantiate
       client_socket.connect((host, port))  # connect to the server
       message = str(file[i])
       print(message)
       client_socket.send(message.encode())  # send message
       data = client_socket.recv(1024).decode()  # receive response
       print('Received from server: ' + data)  # show in terminal
       client_socket.close()
       i = i + 1

         #message = input(" -> ")  # again take input
    print("ended")
    client_socket.close()  # close the connection
    print("ended")

if __name__ == '__main__':
    client_program()