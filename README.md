# Python Programming 
Within this repo is a collection of python practice related to distributed computing in various designs and architectures. 
* Dataset must be [downloaded from kaggle](https://www.kaggle.com/datasets/tylerx/flights-and-airports-data?select=flights.csv) and saved locally

## A1
* aclient-server program using python sockets, capable of manipulating files using various command line commands from the client side. 
* The server is responsible for interpreting the commands and arguments and making the changes to the files or directories.
* After every operation the server updates the client with the latest directory status.
* The client and server communicate using TCP

## A2
* Queries to a large dataset using python pandas. 
* Each query (q1, q2, q3, q4) are written in 3 different techniques (t1, t2, t3)
* Each technique uses a different parallelization implementation: threads, processes, and MPI

## A3
* Demo of a docker cluster executing distributed MPI queries with python
* The list of commands are in the **explanation** files in each task
* T1 involves remote file and directory manipulation
* T2 involves parallel computing using Pandas and MPI

## A4
* Apache Spark with MapReduce to manipulate RDDS (redundant distributed dataframes)
* Data Analysis with various queries.
