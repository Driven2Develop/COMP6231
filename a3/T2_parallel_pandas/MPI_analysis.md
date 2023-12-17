# Analysis of T2
In this section we will compare the behavior of varying the number of workers for an MPI problem. In our environment we have one central master node responsible for delegating tasks to the other workers. In our implementation, technically the master takes a part of the workload as well. Therefore we can excute with exactly one worker -- the master as a single processing script. A graphical representation of the findings can be shown below, where we vary the number of workers for each question. The total time to execute the question is recorded in seconds. Recall the master takes some of the workload so in the below table one of the workers is the master. 


| seconds | Q1 | Q2 | Q3 | Q4 | 
|----------|----------|----------|----------|----------|
| 1 worker | 3.691 | 2.288 | 1.432 | 1.101 | 
| 2 workers | 2.501 | 1.689 | 1.265 | 1.095 | 
| 3 workers | 2.071 | 1.61 | 1.242 | 1.131 |
| 4 workers | 1.896 | 1.555 | 1.293 | 1.251 |
| 5 workers | 1.837 | 1.63 | 1.465 | 1.322 |
| 6 workers | 2.305 | 1.723 | 1.704 | 1.388 |
| 7 workers | 2.207 | 2.137 | 1.758 | 1.678 |
| 8 workers | 2.642 | 1.751 | 2.013 | 1.728 | 
| 9 workers | 3.047 | 1.574 | 2.284 | 1.913 |
| 10 workers | 3.009 | 2.283 | 3.224 | 2.752 |

The data from the timing suggests that the number of workers follows a negative quadratic relation in regards to time. There appears to be an optimal minimum of seconds based on number of workers after which the time increases again. 