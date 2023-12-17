# T2 pandas in parallel

## Instructions for completing Task 2 **(Part A, B, E)** 
Below are the instructions to setup the server side 

1. created network for client and file_server connectivity ```docker network create t2_network```
* We can check the network status with ```docker inspect network dev_network```

2. Initialize the server container and mount the mpi scripts **(Part G)**
* Optionally we can commit the image for the master node ```docker commit file_server ozxx33/mpi4py-cluster-base```
* Committing an image can help with having a reusable image if we make an unintended modification or revert a change. 
```
docker run --name mpi_master -p 65432:65432 --net t2_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T2_parallel_pandas\mpi",target="/mpi_python" --shm-size 2GB -it ozxx33/mpi4py-cluster-base
```

3. Initialize the 3 workers containers with correct volume mounts and network

```
docker run --name mpi_worker1 --security-opt=seccomp:unconfined -p 8080:8080 --net=t2_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T2_parallel_pandas\mpi",target="/mpi_python" --shm-size 30GB -it ozxx33/mpi4py-cluster-base

docker run --name mpi_worker2 --security-opt=seccomp:unconfined -p 8181:8181 --net=t2_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T2_parallel_pandas\mpi",target="/mpi_python" --shm-size 30GB -it ozxx33/mpi4py-cluster-base

docker run --name mpi_worker3 --security-opt=seccomp:unconfined -p 8282:8282 --net=t2_network --mount type=bind,source="C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a3\T2_parallel_pandas\mpi",target="/mpi_python" --shm-size 30GB -it ozxx33/mpi4py-cluster-base
```

4. For each worker:
* Get their IP addresses using ```ifconfig```
* modify their password using ```passwd``` to something memorable for the next instructions
* ensure SSH service is running on the worker container using ```service ssh start```

5. Save IP addresses of the workers on the server (master) machine
* save the IP addresses of workers to a machinefile in ~\ 
* Use ```touch machinefile``` if it does not already exist
* ```echo "[IP address of worker]" >> machinefile``` to store the IP address of workers
* view the file content with ```cat machinefile```

6. Generate an SSH key from to the master to copy to each of the workers
* ```ssh-keygen -t rsa``` and create the key in default directory, and no password
* Copy the ssh key to each of the workers using ```ssh-copy-id -i ~/.ssh/id_rsa.pub root@[IP of worker]``` enter password when prompted
* test to make sure server can ssh to each worker without a password using ```ssh [IP of worker]``` and ```exit``` to return back. 

7. Execute the python scripts using mpi
* Each question's script has already been loaded onto the container. 
* Its output will be showed on the command line, but they can also be viewed on docker desktop
* ```mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q1_t3.py```
* ```mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q2_t3.py```
* ```mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q3_t3.py```
* ```mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q4_t3.py```

8. IP addresses of each worker and their binded ports **(Part D)**
* Worker 1
    * 172.18.0.3 
    * 8080:8080
* Worker 2
    * 172.18.0.4 
    * 8181:8181
* Worker 3
    * 172.18.0.5 
    * 8282:8282

9. Results of each question **(Part E)**
* Q1: Alaska Airlines in 1.981s
* Q2: Empire Airlines Inc. in 1.688s
* Q3: Endeavor Air Inc. in 1.341s
* Q4: 8 in 1.15s

10. Intermediate images
During testing there were some committed images to help with debugging especially for the network communication betweenm containers. However, once the solution was finalized not committed images were required. 

## Log Output for each question **(Part C)**:
The following is a sample output from running the mpi script from the master node. Client logs were unavailable since the mpi work was done in the background. 

### Q1
```
root@34ab12bfafd5:~# mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q1_t3.py 
Worker 3 dispatched with processing dataset from index [225000, 300000].
Results gathered worker 3. Sending to master.
Worker 2 dispatched with processing dataset from index [150000, 225000].
Results gathered worker 2. Sending to master.
Worker 1 dispatched with processing dataset from index [75000, 150000].
Results gathered worker 1. Sending to master.
Worker 0 dispatched with processing dataset from index [0, 75000].
Results gathered worker 0. Sending to master.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3
Results gathered from all workers. Merging.
1.981s -- The airline that had the highest percentage of flights departing from airports with origin codes that start with 'P' or 'S' in 2021 is:
Alaska Airlines Inc. with a percentage of: 92.5898323130157%.
The time it took to compute the solution was 1.981.
```

### Q2
```
root@34ab12bfafd5:~# mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q2_t3.py
Worker 3 dispatched with processing dataset from index [225000, 300000].
Results gathered worker 3. Sending to master.
Worker 2 dispatched with processing dataset from index [150000, 225000].
Results gathered worker 2. Sending to master.
Worker 1 dispatched with processing dataset from index [75000, 150000].
Results gathered worker 1. Sending to master.
Worker 0 dispatched with processing dataset from index [0, 75000].
Results gathered worker 0. Sending to master.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q2 T3
Results gathered from all workers. Merging.
1.688s -- The airline that had the highest percentage of on-time arrivals in 2021 is:
Empire Airlines Inc. with a percentage of: 100.0%.
The time it took to compute the solution was 1.688.
root@34ab12bfafd5:~#
```

### Q3
```
root@34ab12bfafd5:~# mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q3_t3.py
Worker 1 dispatched with processing dataset from index [75000, 150000].
Results gathered worker 1. Sending to master.
Worker 3 dispatched with processing dataset from index [225000, 300000].
Results gathered worker 3. Sending to master.
Worker 2 dispatched with processing dataset from index [150000, 225000].
Results gathered worker 2. Sending to master.
Worker 0 dispatched with processing dataset from index [0, 75000].
Results gathered worker 0. Sending to master.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3
Results gathered from all workers. Merging.
1.341s -- The airline that had the highest percentage of early arrivals in the first quarter (January, February, March) of 2021 is:
Endeavor Air Inc. with a percentage of: 84.06098406098405%.
The time it took to compute the solution was 1.341.
```

### Q4
```
root@34ab12bfafd5:~# mpiexec -n 4 -machinefile machinefile python /mpi_python/scripts/q4_t3.py 
Worker 1 dispatched with processing dataset from index [75000, 150000].
Results gathered worker 1. Sending to master.
Worker 3 dispatched with processing dataset from index [225000, 300000].
Results gathered worker 3. Sending to master.
Worker 2 dispatched with processing dataset from index [150000, 225000].
Results gathered worker 2. Sending to master.
Worker 0 dispatched with processing dataset from index [0, 75000].
Results gathered worker 0. Sending to master.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T3
Results gathered from all workers. Merging.
1.15s -- The busiest hour at ATL airport during November 2021 is:
8 with 49 flights.
The time it took to compute the solution was 1.15.
```