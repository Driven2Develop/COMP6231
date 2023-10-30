# SAMPLE OUTPUT
## Q1 T1

```
PS C:\Workspace\School\fall-2023\COMP6231_Distributed_Systems\homework\a2\Assignment_2_handout\implementation\q1> python .\t1.py                                                             
1698630685.636s: Processing flights data of size 6311871 with 4 threads.
Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q1 T1
0.0s -- Loading csv file, and filtering based on acceptance criteria.
16.095s -- Dataframe loaded.
16.095s -- Finding all unique airline names.
20.699s -- All unique airline names found.
20.7s -- Thread: 0 -- Processing part of filtered CSV file from index 0 to 321210.
20.7s -- Thread: 1 -- Processing part of filtered CSV file from index 321210 to 642420.
20.73s -- Thread: 2 -- Processing part of filtered CSV file from index 642420 to 963629.
20.763s -- Thread: 3 -- Processing part of filtered CSV file from index 963629 to 1284838.
245.633s -- Thread: 0 -- Processing finished, terminating thread.
245.668s -- Thread: 1 -- Processing finished, terminating thread.
245.688s -- Thread: 2 -- Processing finished, terminating thread.
245.714s -- Thread: 3 -- Processing finished, terminating thread.
245.714s -- The airline that had the highest percentage of flights departing from airports with origin codes that start with 'P' or 'S' in 2021 is:
Alaska Airlines Inc. with a percentage of: 56.24619618427668%.
The time it took to compute the solution was 245.715 seconds. With 4 threads.
```

## Q1 T2

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

## Q1 T3
## Q2 T1

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

## Q2 T2

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
## Q2 T3
## Q3 T1

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
## Q3 T2
## Q3 T3
## Q4 T1
## Q4 T2
## Q4 T3
