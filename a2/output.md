# SAMPLE OUTPUT
## Q1 T1 [GOOD]

```
1698797160.742s: Processing flights data of size 6311871 with 4 threads.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T1
0.0s -- Loading csv file, and filtering based on acceptance criteria.
18.782s -- Dataframe loaded.
18.783s -- Finding all unique airline names.
23.139s -- All unique airline names found.
23.144s -- Thread: 0 -- Processing part of filtered CSV file from index 0 to 321210.
23.155s -- Thread: 1 -- Processing part of filtered CSV file from index 321210 to 642420.
23.189s -- Thread: 2 -- Processing part of filtered CSV file from index 642420 to 963629.
23.195s -- Thread: 3 -- Processing part of filtered CSV file from index 963629 to 1284838.
884.409s -- Thread: 1 -- Processing finished, terminating thread.
884.622s -- Thread: 3 -- Processing finished, terminating thread.
884.646s -- Thread: 0 -- Processing finished, terminating thread.
884.715s -- Thread: 2 -- Processing finished, terminating thread.
884.727s -- The airline that had the highest percentage of flights departing from airports with origin codes that start with 'P' or 'S' in 2021 is:
Horizon Air with a percentage of: 58.11534740387716%.
The time it took to compute the solution was 884.727 seconds. With 4 threads.
```

## Q1 T2 [GOOD]

```
PS C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q1> python .\t2.py
1698681148.111s: Processing flights data of size 6311871 with 4 processes.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T2
0.0s -- Loading csv file and calculating chunk size.
13.669s -- CSV file loaded. Chunk size is 1577967.
13.671s -- Creating pools for chunk processing.
30.544s -- All processes completed in pools
30.545s -- The airline that had the highest percentage of flights departing from airports with origin codes that start with 'P' or 'S' in 2021 is:
Horizon Air with a percentage of: 58.11534740387716%.
The time it took to compute the solution was 30.546 seconds. With 4 processes.
```

## Q1 T3 [GOOD]

```
$ mpiexec -n 4 python t3.py
1698948705.377s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3
Counting flights for chunk with size 1577970
Finished Counting flights for chunk with size 1577970
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q1\t3.py", line 93, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948705.699s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q1\t3.py", line 93, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948705.696s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q1\t3.py", line 93, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948705.694s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
33.243s -- The airline that had the highest percentage of flights departing from airports with origin codes that start with 'P' or 'S' in 2021 is:
Horizon Air with a percentage of: 58.11534740387716%.
```
## Q2 T1 [GOOD]

```
PS C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q2> python .\t1.py
1698630751.817s: Processing flights data of size 6311871 with 4 threads.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q2 T1
0.0s -- Loading csv file, and filtering based on acceptance criteria.
15.601s -- Dataframe loaded.
15.602s -- Finding all unique airline names.
20.359s -- All unique airline names found.
20.361s -- Thread: 0 -- Processing part of filtered CSV file from index 0 to 1073100.
20.361s -- Thread: 1 -- Processing part of filtered CSV file from index 1073100 to 2146200.
20.373s -- Thread: 2 -- Processing part of filtered CSV file from index 2146200 to 3219300.
20.405s -- Thread: 3 -- Processing part of filtered CSV file from index 3219300 to 4292399.
1168.325s -- Thread: 0 -- Processing finished, terminating thread.
1169.207s -- Thread: 1 -- Processing finished, terminating thread.
1169.212s -- Thread: 2 -- Processing finished, terminating thread.
1169.271s -- Thread: 3 -- Processing finished, terminating thread.
1169.271s -- The airline that had the highest percentage of on-time arrivals in 2021 is :
Endeavor Air Inc. with a percentage of: 84.09882076090337%.
The time it took to compute the solution was 1169.272 seconds. With 4 threads.
```

## Q2 T2 [GOOD]

```
PS C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q2> python .\t2.py
1698681302.495s: Processing flights data of size 6311871 with 4 processes.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q2 T2
0.0s -- Loading csv file and calculating chunk size.
13.987s -- CSV file loaded. Chunk size is 1577967.
13.987s -- Creating pools for chunk processing.
22.285s -- All processes completed in pools
22.286s -- The airline that had the highest percentage of on-time arrivals in 2021 is:
Endeavor Air Inc. with a percentage of: 81.399%.
The time it took to compute the solution was 22.286 seconds. With 4 processes.
```
## Q2 T3 [GOOD]

```
$ mpiexec -n 4 python t3.py
1698948972.695s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3      
Counting flights for chunk with size 1577970
Finished Counting flights for chunk with size 1577970
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q2\t3.py", line 91, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948972.718s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3      
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q2\t3.py", line 91, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948972.86s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T3      
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q2\t3.py", line 91, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698948972.801s: Processing flights data of size 6311871.
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
23.26s -- The airline that had the highest percentage of on-time arrivals in 2021 is:
Endeavor Air Inc. with a percentage of: 81.39859930227416%.
The time it took to compute the solution was 23.26.
```
## Q3 T1 [GOOD]

```
PS C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q3> python .\t1.py
1698630907.875s: Processing flights data of size 6311871 with 4 threads.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q2 T1
0.0s -- Loading csv file, and filtering based on acceptance criteria.
15.791s -- Dataframe loaded.
15.792s -- Finding all unique airline names.
20.905s -- All unique airline names found.
20.907s -- Thread: 0 -- Processing part of filtered CSV file from index 0 to 0.
20.907s -- Thread: 1 -- Processing part of filtered CSV file from index 0 to 0.
20.908s -- Thread: 1 -- Processing finished, terminating thread.
20.908s -- Thread: 2 -- Processing part of filtered CSV file from index 0 to 0.
20.907s -- Thread: 0 -- Processing finished, terminating thread.
20.908s -- Thread: 3 -- Processing part of filtered CSV file from index 0 to 0.
20.909s -- Thread: 3 -- Processing finished, terminating thread.
20.909s -- Thread: 2 -- Processing finished, terminating thread.
20.909s -- The airline that had the highest percentage of early arrivals in the first quarter of 2021 is :
SkyWest Airlines Inc. with a percentage of: 0.0%.
The time it took to compute the solution was 20.909 seconds. With 4 threads.
```
## Q3 T2 [GOOD]

```
1698808462.782s: Processing flights data of size 6311871 with 4 processes.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T2
0.0s -- Loading csv file and calculating chunk size.
13.484s -- CSV file loaded. Chunk size is 1577967.
13.486s -- Creating pools for chunk processing.
24.674s -- All processes completed in pools
24.675s -- The airline that had the highest percentage of early arrivals in the first quarter (January, February, March) of 2021 is:
Empire Airlines Inc. with a percentage of: 75.89285714285714%.
The time it took to compute the solution was 24.676 seconds. With 4 processes.
```
## Q3 T3 [GOOD]

```
$ mpiexec -n 4 python t3.py 
1698949502.216s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3
Counting flights for chunk with size 1577970
Finished Counting flights for chunk with size 1577970
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q3\t3.py", line 96, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698949502.318s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q3\t3.py", line 96, in <module>
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
1698949502.411s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
Traceback (most recent call last):
  File "C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q3\t3.py", line 96, in <module>
1698949502.42s: Processing flights data of size 6311871.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3
Counting flights for chunk with size 1577967
Finished Counting flights for chunk with size 1577967
25.497s -- The airline that had the highest percentage of early arrivals in the first quarter (January, February, March) of 2021 is:
Empire Airlines Inc. with a percentage of: 75.89285714285714%.
The time it took to compute the solution was 25.497.
    answer, timetaken = solution.run()
TypeError: cannot unpack non-iterable NoneType object
```
## Q4 T1 [GOOD]

```
1698809241.858s: Processing flights data of size 6311871 with 4 threads.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T1
0.0s -- Loading csv file, and filtering based on acceptance criteria.
16.209s -- Dataframe loaded.
16.214s -- Thread: 0 -- Processing part of filtered CSV file from index 0 to 6652.
16.214s -- Thread: 1 -- Processing part of filtered CSV file from index 6652 to 13303.
16.36s -- Thread: 2 -- Processing part of filtered CSV file from index 13303 to 19954.
16.611s -- Thread: 3 -- Processing part of filtered CSV file from index 19954 to 26605.
21.547s -- Thread: 2 -- Processing finished, terminating thread.
21.991s -- Thread: 0 -- Processing finished, terminating thread.
22.392s -- Thread: 1 -- Processing finished, terminating thread.
22.491s -- Thread: 3 -- Processing finished, terminating thread.
22.492s -- The busiest hour at ATL airport during November 2021 is:
8 with 2518 flights.
The time it took to compute the solution was 22.493 seconds. With 4 threads.
```
## Q4 T2 [GOOD]

```
1698944744.081s: Processing flights data of size 6311871 with 4 processes.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T2
0.0s -- Loading csv file and calculating chunk size.
14.909s -- CSV file loaded. Chunk size is 1577967.
14.911s -- Creating pools for chunk processing.
21.405s -- All processes completed in pools
21.406s -- The busiest hour at ATL airport during November 2021 is:
8 with 2518 flights.
The time it took to compute the solution was 21.406 seconds. With 4 processes.
```
## Q4 T3 [GOOD]

```
$ mpiexec -n 4 python t3.py
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T3
18.999s -- The busiest hour at ATL airport during November 2021 is:
8 with 2518 flights.
The time it took to compute the solution was 18.999.
```