import socket
import os
import sys


"""
    Same implementation as in receive_message_ending_with_token() in server.py
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

        if packet.decode()[-len(eof_token):] == eof_token.decode():
            data = data[:-len(eof_token)].decode()
            break
    
    return data 

def send_message_ending_with_token(active_socket, message, eof_token):
    active_socket.sendall(str.encode(message + eof_token.decode()))

"""
    1) Creates a socket object and connects to the server.
    2) receives the random token (10 bytes) used to indicate end of messages.
    3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param host: the ip address of the server
    :param port: the port number of the server
    :return: the created socket object
"""
def initialize(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    eof_token = s.recv(1024)
    print('Connected to server at IP:', host, 'and Port:', port)
    print('Handshake Done. EOF is:', eof_token)
    print(receive_message_ending_with_token(s, 1024, eof_token))

    return s, eof_token

"""
    Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
"""
def issue_cd(command_and_arg, client_socket, eof_token):
    send_message_ending_with_token(client_socket, command_and_arg, eof_token)  
    print(receive_message_ending_with_token(client_socket, 1024, eof_token))

"""
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
"""
def issue_mkdir(command_and_arg, client_socket, eof_token):
    send_message_ending_with_token(client_socket, command_and_arg, eof_token)
    print(receive_message_ending_with_token(client_socket, 1024, eof_token))

"""
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
"""
def issue_rm(command_and_arg, client_socket, eof_token):
    send_message_ending_with_token(client_socket, command_and_arg, eof_token)
    print(receive_message_ending_with_token(client_socket, 1024, eof_token))

"""
    Sends the full ul command entered by the user to the server. 
    Then, it reads the file to be uploaded as binary and sends it to the server. 
    The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
"""
def issue_ul(command_and_arg, client_socket, eof_token):
    file_name = command_and_arg[len('ul'):].strip()
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.isfile(file_path): #check existance of file
        print("Invalid entry. You entered a nonexistant filename! Exiting operation.")
        return
    
    send_message_ending_with_token(client_socket, command_and_arg, eof_token)

    with open(file_path, 'rb') as file:
        content = file.read()
        while content:
            client_socket.sendall(str(content).encode())
            content = file.read()
    
    client_socket.sendall(eof_token);
    print("Successfully sent file {} to server".format(file_name))    
    print(receive_message_ending_with_token(client_socket, 1024, eof_token))

"""
    Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
    socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
    the server.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return:
"""
def issue_dl(command_and_arg, client_socket, eof_token):
    file_name = command_and_arg[len('dl'):].strip()

    if os.path.isfile(file_name):
        print("Invalid entry. File with name {file_name} already exists in cwd. Exiting operation.")
        return
    
    send_message_ending_with_token(client_socket, command_and_arg, eof_token) 

    with open(os.path.join(os.path.dirname(__file__), file_name), 'w') as file:
        content = receive_message_ending_with_token(client_socket, 1024, eof_token)
        file.write(content)
    
    print("Successfully recieved file from server. New filename is {}.".format(file_name))

def main():

    # The server's hostname or IP address
    arguments = sys.argv[1:]

    if len(arguments) >= 1:
         HOST = arguments[0]
    else:
        HOST = "file_server"
    PORT = 65432  # The port used by the server
    s, eof_token = initialize(HOST, PORT)

    command_dict = {
        'cd': issue_cd,
        'mkdir': issue_mkdir,
        'rm': issue_rm,
        'ul': issue_ul,
        'dl': issue_dl
    }

    while True: #main execution loop

        # get user input
        user_input = input("Please provide some commands and arguments, separated by a space ").lower()
        
        # call the corresponding command function or exit
        if user_input == 'exit':
            send_message_ending_with_token(s, 'exit', eof_token)
            break
        cmd = user_input.split(" ")[0]
        if cmd in command_dict:
            print("Issuing {} command to server.".format(cmd))
            command_dict[cmd](user_input, s, eof_token)
        else:
            print("Command not recognized, please try again. Command must start with: cd, mkdir, rm, ul, or dl.\n")
        
    print('Closing socket and exiting the application.')
    s.close()

if __name__ == '__main__':
    main()