"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q4 T3

Find the airline that had the highest percentage of flights arriving early (with a
negative arrival delay) in the first quarter of 2021.
"""
import math
import time
from mpi4py import MPI 
import pandas as pd
import os
   
class MPISolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, dataset_path=None, dataset_size=None):
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.airlines = [] # list of custom airline objects
        self.start_time = time.time()
        self.dataset_columns = ["FlightDate", "Airline", "ArrDelay", "DepTime", "Origin"] # only import the columns that are necessary 
        self.num_of_flight_by_hour = [0] * 24

    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    """
    def run(self):

        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        chunk_size = self.dataset_size//size # calculate chunk size based on number of workers
        df = pd.read_csv(self.dataset_path, usecols = self.dataset_columns)

        start = rank * chunk_size
        end = start + chunk_size if rank < size - 1 else self.dataset_size
        
        print("Worker {} dispatched with processing dataset from index [{}, {}].".format(rank, start, end))
        results = comm.gather(self.count_flights(df.iloc[start:end]), root=0)
        print(f"Results gathered worker {rank}. Sending to master.")

        if rank == 0:
            print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T3")

            # merge results from workers
            self.num_of_flight_by_hour = [sum(row[i] for row in results) for i in range(len(results[0]))]
            print("Results gathered from all workers. Merging.")

            # return max
            max_hour = self.num_of_flight_by_hour.index(max(self.num_of_flight_by_hour))
            print("{}s -- The busiest hour at ATL airport during November 2021 is:\n{} with {} flights.".format(round(time.time() - self.start_time, 3), max_hour, max(self.num_of_flight_by_hour)))
            print("The time it took to compute the solution was {}.".format(round((time.time() - self.start_time), 3)))
            return max_hour, (time.time() - self.start_time)
        else:
            return 0, 0
    # counts flights and groups based on airline
    def count_flights(self, chunk):
        
        num_of_flights = [0] *24
        filter = ((pd.to_datetime(chunk["FlightDate"]).dt.year == 2021) & (pd.to_datetime(chunk["FlightDate"]).dt.month == 11) & (chunk["Origin"] == 'ATL'))  
        chunk = chunk[filter]

        for index, row in chunk.iterrows(): 
            if (math.isnan(row["DepTime"])): # skip if deptime is NaN
                continue
            
            num_of_flights[int(row["DepTime"]//100)] +=1
        
        return num_of_flights
    
if __name__ == '__main__':
    dataset_filename = "sampled_flights_data_300k.csv"
    dataset_dir = "datasets"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dataset_dir, dataset_filename)
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))

    solution = MPISolution(dataset_path=dataset_path, dataset_size=dataset_size) #total should be about 6311871
    answer, timetaken = solution.run()