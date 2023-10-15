import socket
import os

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.eof_token = None
    
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
        :return: the eof_token
    """
    def initialize(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        
        self.eof_token = self.client_socket.recv(1024)
        print('Connected to server at IP:', host, 'and Port:', port)
        print('Handshake Done. EOF is:', self.eof_token)
        print(self.receive_message_ending_with_token(self.client_socket, 1024, self.eof_token))

        return self.client_socket, eof_token

    """
    Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    def issue_cd(self, command_and_arg, client_socket, eof_token):
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)  
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))

    """
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    def issue_mkdir(self, command_and_arg, client_socket, eof_token):
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))

    """
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    def issue_rm(self, command_and_arg, client_socket, eof_token):
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))

    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    def issue_ul(self, command_and_arg, client_socket, eof_token):
        file_name = command_and_arg[len('ul'):].strip()
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if not os.path.isfile(file_path): #check existance of file
            print("Invalid entry. You entered a nonexistant filename! Exiting operation.")
            return
        
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)

        with open(file_path, 'rb') as file:
            content = file.read()
            while content:
                client_socket.sendall(str(content).encode())
                content = file.read()
        
        client_socket.sendall(eof_token);
        print("Successfully sent file {} to server".format(file_name))    
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))

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
    def issue_dl(self, command_and_arg, client_socket, eof_token):
        file_name = command_and_arg[len('dl'):].strip()

        if os.path.isfile(file_name):
            print("Invalid entry. File with name {file_name} already exists in cwd. Exiting operation.")
            return
        
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token) 

        with open(os.path.join(os.path.dirname(__file__), file_name), 'w') as file:
            content = self.receive_message_ending_with_token(client_socket, 1024, eof_token)
            file.write(content)
    
        print("Successfully recieved file from server. New filename is {}.".format(file_name))
    
    """
    Sends the full info command entered by the user to the server. The server reads the file and sends back the size of
    the file.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return: the size of file in string
    """
    def issue_info(self,command_and_arg, client_socket, eof_token):
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))

    """
    Sends the full mv command entered by the user to the server. The server moves the file to the specified directory and sends back
    the updated. This command can also act as renaming the file in the same directory. 
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    def issue_mv(self,command_and_arg, client_socket, eof_token):
        self.send_message_ending_with_token(client_socket, command_and_arg, eof_token)
        print(self.receive_message_ending_with_token(client_socket, 1024, eof_token))


    def start(self):
        """
        1) Initialization
        2) Accepts user input and issue commands until exit.
        """
        command_dict = {
            'cd': self.issue_cd,
            'mkdir': self.issue_mkdir,
            'rm': self.issue_rm,
            'ul': self.issue_ul,
            'dl': self.issue_dl,
            'info': self.issue_info,
            'mv': self.issue_mv
        }
        self.initialize(self.host, self.port)

        while True: #main execution loop

            # get user input
            user_input = input("Please provide some commands and arguments, separated by a space >").lower()
            
            # call the corresponding command function or exit
            if user_input == 'exit':
                self.send_message_ending_with_token(self.client_socket, 'exit', self.eof_token)
                break
            cmd = user_input.split(" ")[0]
            if cmd in command_dict:
                print("Issuing {} command to server.".format(cmd))
                command_dict[cmd](user_input, self.client_socket, self.eof_token)
            else:
                print("Command not recognized, please try again. Command must start with: cd, mkdir, rm, ul, or dl.\n")
            
        print('Closing socket and exiting the application.')
        self.client_socket.close()


def run_client():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    client = Client(HOST, PORT)
    client.start()


if __name__ == '__main__':
    run_client()
