# T1 file server

## Instructions to complete Task 1 **(Part E, F) **
1. create network for client and file_server connectivity ```docker network create dev_network```
* We can check the network status with ```docker inspect network dev_network```

2. Initialize the server and start server python script, the server should be listening for connections
```
docker run --name file_server -p 65432:65432 --net dev_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T1_file_server\server.py",target="/scripts/server.py" --shm-size 2GB -it ozxx33/fileserver-base 
```
* Start the server Python script with ```python scripts/server.py```
* The server should now be listening for connections

3. Commit the server's image **(Part G)**
* We typically commit images to reuse them during debugging ```docker commit file_server ozxx33/fileserver-base```
* the commits capture the image during a certain status such as volumes, networks, or other parameters. 
* If we make a mistake we can always revert back to a committed image.  


4. start clients on the same network as the server
```
docker run --name client1 --security-opt=seccomp:unconfined -p 8080:8080 --net=dev_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T1_file_server\client.py",target="/scripts/client.py" --shm-size 30GB -it ozxx33/fileserver-base

docker run --name client2 --security-opt=seccomp:unconfined -p 8181:8181 --net=dev_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T1_file_server\client.py",target="/scripts/client.py" --shm-size 30GB -it ozxx33/fileserver-base

docker run --name client3 --security-opt=seccomp:unconfined -p 8282:8282 --net=dev_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T1_file_server\client.py",target="/scripts/client.py" --shm-size 30GB -it ozxx33/fileserver-base
```
* navigate to the python file located in the /scripts directory
* be sure to specify the server IP before running the client.py [server IP address]

## Sockets used **(Part D)**
* Server:
    * Port Binding 65432:65432
    * Listening 0.0.0.0:65432
* Client 1: 
    * Port Binding 8080:8080
    * Connecting to 172.17.0.2:65432
* Client 2: 
    * Port Binding 8181:8181
    * Connecting to 172.17.0.2:65432
* Client 3: 
    * Port Binding 8282:8282
    * Connecting to 172.17.0.2:65432

## Sample output logs **(Part A, B, C)**
Logs can be obtained from docker desktop, or  with the command ```docker logs mpi_container_1``` or directly on the container. The following Logs were obtaining from executing instructions in Part A and B. 

### Server
```
root@4fce32b5b3bb:/# python scripts/server.py
Server binded to host 0.0.0.0 on port 65432. Listening for connections...
Connected by address: ('172.22.0.2', 43090). Creating new client thread.
Connection from :  ('172.22.0.2', 43090)
Client ('172.22.0.2', 43090) disconnected. Closing socket.
Awaiting more client connections...
Connected by address: ('172.22.0.4', 50760). Creating new client thread.
Connection from :  ('172.22.0.4', 50760)
Client ('172.22.0.4', 50760) disconnected. Closing socket.
Awaiting more client connections...
Connected by address: ('172.22.0.5', 54312). Creating new client thread.
Connection from :  ('172.22.0.5', 54312)
Client ('172.22.0.5', 54312) disconnected. Closing socket.
Awaiting more client connections...
```

### Client 1
```
root@1b53255812d7:/# python scripts/client.py 172.22.0.3
Connected to server at IP: 172.22.0.3 and Port: 65432
Handshake Done. EOF is: b'<40e7c619b3ae3747>'
Current Directory: //scripts:
|
--
-- server.py
Please provide some commands and arguments, separated by a space mkdir client1
Issuing mkdir command to server.
Current Directory: //scripts:
|
-- client1
-- server.py
Please provide some commands and arguments, separated by a space cd client1
Issuing cd command to server.
Current Directory: //scripts/client1:
|
--
--
Please provide some commands and arguments, separated by a space mkdir new-dir-demo
Issuing mkdir command to server.
Current Directory: //scripts/client1:
|
-- new-dir-demo
--
Please provide some commands and arguments, separated by a space cd ..
Issuing cd command to server.
Current Directory: //scripts:
|
-- client1
-- server.py
Please provide some commands and arguments, separated by a space exit
Closing socket and exiting the application.
```
### Client 2
```
root@0ed4d95bc9ee:/# python scripts/client.py 172.22.0.3
Connected to server at IP: 172.22.0.3 and Port: 65432
Handshake Done. EOF is: b'<9577354fc0915532>'
Current Directory: //scripts:
|
-- client1
-- server.py
Please provide some commands and arguments, separated by a space mkdir client2
Issuing mkdir command to server.
Current Directory: //scripts:
|
-- client1
-- client2
-- server.py
Please provide some commands and arguments, separated by a space cd client2
Issuing cd command to server.
Current Directory: //scripts/client2:
|
--
--
Please provide some commands and arguments, separated by a space mkdir new-dir-demo
Issuing mkdir command to server.
Current Directory: //scripts/client2:
|
-- new-dir-demo
--
Please provide some commands and arguments, separated by a space cd ..
Issuing cd command to server.
Current Directory: //scripts:
|
-- client1
-- client2
-- server.py
Please provide some commands and arguments, separated by a space exit
Closing socket and exiting the application.
```
### Client 3

```
root@3bf8ed7d7f05:/# python scripts/client.py 172.22.0.3
Connected to server at IP: 172.22.0.3 and Port: 65432
Handshake Done. EOF is: b'<3b12109313b88e46>'
Current Directory: //scripts:
|
-- client1
-- client2
-- server.py
Please provide some commands and arguments, separated by a space mkdir client3
Issuing mkdir command to server.
Current Directory: //scripts:
|
-- client1
-- client3
-- client2
-- server.py
Please provide some commands and arguments, separated by a space cd client3
Issuing cd command to server.
Current Directory: //scripts/client3:
|
--
--
Please provide some commands and arguments, separated by a space mkdir new-dir-demo
Issuing mkdir command to server.
Current Directory: //scripts/client3:
|
-- new-dir-demo
--
Please provide some commands and arguments, separated by a space cd ..
Issuing cd command to server.
Current Directory: //scripts:
|
-- client1
-- client3
-- client2
-- server.py
Please provide some commands and arguments, separated by a space exit
Closing socket and exiting the application.
```