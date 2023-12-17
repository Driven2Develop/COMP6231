import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
import secrets
import sys

"""
Creates a string representation of a working directory and its contents.
:param working_directory: path to the directory
:return: string of the directory and its contents.
"""
def get_working_directory_info(working_directory):
    dirs = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_dir()])
    files = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_file()])
    dir_info = f'Current Directory: {working_directory}:\n|{dirs}{files}'
    return dir_info

"""
Helper method to generates a random token that starts with '<' and ends with '>'.
The total length of the token (including '<' and '>') should be 10.
Examples: '<1f56xc5d>', '<KfOVnVMV>'
return: the generated token.
"""
def generate_random_eof_token(eof_token_length=10):
    eof = secrets.token_bytes(eof_token_length - 2).hex()
    return '<' + eof + '>'

"""
    Same implementation as in receive_message_ending_with_token() in client.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
"""
def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    data = bytearray()
    while True:                             # keep receiving until we get '<EOF>'
        packet = active_socket.recv(buffer_size)
        data.extend(packet)

        if packet.decode()[-len(eof_token):] == eof_token:
            data = data[:-len(eof_token)]
            break
    
    return data 

def send_message_ending_with_token(active_socket, message, eof_token):
    active_socket.sendall(str.encode(message + eof_token))

"""
    Handles the client cd commands. Reads the client command and changes the current_working_directory variable 
    accordingly. Returns the absolute path of the new current working directory.
    :param current_working_directory: string of current working directory
    :param new_working_directory: name of the sub directory or '..' for parent
    :return: absolute path of new current working directory
"""
def handle_cd(current_working_directory, new_working_directory):
    if (new_working_directory == ".."):
        return os.path.dirname(current_working_directory)
    
    if (new_working_directory not in os.listdir(current_working_directory)):
        print("Invalid entry. No child directory matches new working directory.")
        return current_working_directory
    else:
        return os.path.join(current_working_directory, new_working_directory)

"""
    Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
    :param current_working_directory: string of current working directory
    :param directory_name: name of new sub directory
"""  
def handle_mkdir(current_working_directory, directory_name):
    allowed = True;
    invalid_char = ['<', '>', ':', '/', '\\', '|', '?', '*']
    for c in directory_name:
        if c in invalid_char:
            allowed = False

    if (len(directory_name) > 260 or not allowed ):
        print("Invalid entry. Directory name contains illegal characters, or is too large.")
        return

    os.chdir(current_working_directory)
    os.makedirs(directory_name)

"""
    Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
    based on the object type (directory/file).
    :param current_working_directory: string of current working directory
    :param object_name: name of sub directory or file to remove
"""
def handle_rm(current_working_directory, object_name):
    
    os.chdir(current_working_directory)

    if os.path.isfile(object_name):
        print("Removing file: {}".format(object_name))
        os.remove(object_name)
    elif os.path.isdir(object_name):
        print("Removing directory and all subfolders: {}".format(object_name))
        os.rmdir(object_name)
    else:
        print("Invalid entry. {} is neither a path nor a directory. Aborting operation.".format(object_name))

"""
    Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
    file in the current working directory.
    Use the helper method: receive_message_ending_with_token() to receive the message from the client.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be created.
    :param service_socket: active socket with the client to read the payload/contents from.
    :param eof_token: a token to indicate the end of the message.
"""
def handle_ul(current_working_directory, file_name, service_socket, eof_token):
    
    with open(os.path.join(current_working_directory, file_name), 'w') as file:
        content = receive_message_ending_with_token(service_socket, 1024, eof_token).decode()
        file.write(content)
    
    print("Successfully recieved file from client. New fileneame is: {}".format(file_name))

"""
    Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
    given socket.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be sent to client
    :param service_socket: active service socket with the client
    :param eof_token: a token to indicate the end of the message.
"""
def handle_dl(current_working_directory, file_name, service_socket, eof_token):
    
    with open(os.path.join(current_working_directory, file_name), 'rb') as file:
        content = file.read()
        while content:
            service_socket.sendall(str(content).encode())
            content = file.read()
    
    service_socket.sendall(str(eof_token).encode())
    print("Successfully sent file {} to client.".format(file_name))

"""
Object representing client thread. 
Contains reference to cwd and eof for each client.
"""
class ClientThread(Thread):

    def __init__(self, service_socket : socket.socket, address : str):
        Thread.__init__(self)
        self.service_socket = service_socket
        self.address = address
        self.cwd = os.path.dirname(__file__);
        self.eof_token = generate_random_eof_token();

    def exit(self):
        print("Client {} disconnected. Closing socket.".format(self.address))
        self.service_socket.close()
    
    def run(self):
        print ("Connection from : ", self.address)

        # initialize the connection and send random eof token
        self.service_socket.sendall(str.encode(self.eof_token))

        # establish current working directory and send info        
        send_message_ending_with_token(self.service_socket, get_working_directory_info(self.cwd), self.eof_token)
        
        #main execution loop
        while True:
            client_message = receive_message_ending_with_token(self.service_socket, 1024, self.eof_token).decode()
            
            # get the command and arguments and call the corresponding method
            cmd = client_message.split(" ")[0].strip().lower()

            if cmd == "cd":
                self.cwd = handle_cd(self.cwd, client_message[len('cd'):].strip().lower() )
            elif cmd == "mkdir":
                handle_mkdir(self.cwd, client_message[len('mkdir'):].strip().lower())
            elif cmd == "rm":
                handle_rm(self.cwd, client_message[len('rm'):].strip().lower())
            elif cmd == "ul":
                handle_ul(self.cwd, client_message[len('ul'):].strip().lower(), self.service_socket, self.eof_token)
            elif cmd == "dl":
                handle_dl(self.cwd, client_message[len('dl'):].strip().lower(), self.service_socket, self.eof_token)
            elif cmd == "exit":
                break
            
            # after every operation, send current dir info
            send_message_ending_with_token(self.service_socket, get_working_directory_info(self.cwd), self.eof_token)
        
        self.exit()

def main():
    # # The server's hostname or IP address
    # arguments = sys.argv[1:]

    # if len(arguments) >= 1:
    #     HOST = arguments[0]
    # else:
    HOST = "0.0.0.0"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server binded to host {} on port {}. Listening for connections...".format(HOST, PORT))

        while True:
            conn, addr = s.accept() # client is connected, so create new thread

            print("Connected by address: {}. Creating new client thread.".format(addr))
            thread = ClientThread(conn, addr)
            thread.run()

            print("Awaiting more client connections...")

if __name__ == '__main__':
    main()