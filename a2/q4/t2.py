"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q4 T2

Find the airline that had the highest percentage of flights arriving early (with a
negative arrival delay) in the first quarter of 2021.
"""
import math
import time
import multiprocessing
import pandas as pd
import os

class MultiProcessingSolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, num_of_processes=None, dataset_path=None, dataset_size=None):
        self.num_of_processes = num_of_processes
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.start_time = time.time()
        self.dataset_columns = ["FlightDate", "Airline", "ArrDelay", "DepTime", "Origin"]
        self.num_of_flight_by_hour = [0] * 24
    
    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    Uses either the total number of processes provided by user, or what is avaiable on hardware. Whichever is smaller.
    """
    def run(self):
        print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T2")

        # load csv and filter based on acceptance criteria
        print("{}s -- Loading csv file and calculating chunk size.".format(round(time.time() - self.start_time, 3)))
        df = pd.read_csv(self.dataset_path, usecols = self.dataset_columns)

        # calculate chunk size based on number of pools
        chunk_size = len(df)//self.num_of_processes

        print("{}s -- CSV file loaded. Chunk size is {}.".format(round(time.time() - self.start_time, 3), chunk_size))
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

        print("{}s -- Creating pools for chunk processing.".format(round(time.time() - self.start_time, 3)))
        pool = multiprocessing.Pool(processes=self.num_of_processes)
        results = pool.map(self.count_flights, chunks)

        # cleanup pools
        pool.close()
        pool.join()

        print("{}s -- All processes completed in pools".format(round(time.time() - self.start_time, 3)))

        # merge results together
        self.num_of_flight_by_hour = [sum(row[i] for row in results) for i in range(len(results[0]))]

        # return max
        max_hour = self.num_of_flight_by_hour.index(max(self.num_of_flight_by_hour))
        print("{}s -- The busiest hour at ATL airport during November 2021 is:\n{} with {} flights.".format(round(time.time() - self.start_time, 3), max_hour, max(self.num_of_flight_by_hour)))

        return max_hour, (time.time() - self.start_time)

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
    dataset_filename = "Combined_Flights_2021.csv"
    dataset_dir = "dataset"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.join(dataset_dir, dataset_filename))
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))
    num_of_processes = 4

    print("{}s: Processing flights data of size {} with {} processes.".format(round(time.time(), 3), dataset_size, num_of_processes))
    solution = MultiProcessingSolution(num_of_processes=num_of_processes, dataset_path=dataset_path, dataset_size=dataset_size) #total should be about 6311871
    answer, timetaken = solution.run()
    print("The time it took to compute the solution was {} seconds. With {} processes.".format(round(timetaken, 3), num_of_processes))