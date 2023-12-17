"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q3 T3

Find the airline that had the highest percentage of flights arriving early (with a
negative arrival delay) in the first quarter of 2021.
"""
import time
from mpi4py import MPI 
import pandas as pd
import os
from itertools import chain

"""
Custom Airline object for count tracking, and percentage calculations
"""
class Airline:
    def __init__(self, flights=0, early_arrivals=0, name=None):
        self.flights = flights
        self.early_arrivals = early_arrivals
        self.name = name
    
    def get_percentage(self):
        return (self.early_arrivals/self.flights)*100
    
class MPISolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, dataset_path=None, dataset_size=None):
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.airlines = [] # list of custom airline objects
        self.start_time = time.time()
        self.dataset_columns = ["FlightDate", "Airline", "ArrDelay", "Quarter"] # only import the columns that are necessary 

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
            print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T3")

            # merge results from workers
            results = list(chain.from_iterable(results))
            print("Results gathered from all workers. Merging.")

            for airline in results:
                if airline.name in [airline.name for airline in self.airlines]:
                    [a for a in self.airlines if a.name == airline.name][0].early_arrivals += airline.early_arrivals
                    [a for a in self.airlines if a.name == airline.name][0].flights += airline.flights
                else:
                    self.airlines.append(Airline(airline.flights, airline.early_arrivals, airline.name))
    
            # return max
            max_airline = max(self.airlines, key=lambda airline: airline.get_percentage())
            print("{}s -- The airline that had the highest percentage of early arrivals in the first quarter (January, February, March) of 2021 is:\n{} with a percentage of: {}%.".format(round(time.time() - self.start_time, 3), max_airline.name, max_airline.get_percentage()))
            print("The time it took to compute the solution was {}.".format(round((time.time() - self.start_time), 3)))
            return max_airline.name, (time.time() - self.start_time)
        else:
            return "", 0
        
    # counts flights and groups based on airline
    def count_flights(self, chunk):
        airlines = []

        for airline in chunk['Airline'].unique():
            flight_count = ((chunk['Airline'] == airline) & (chunk["Quarter"] == 1)).sum()
            dep_count = ((chunk["Quarter"] == 1) & (chunk['ArrDelay'] < 0) & (chunk['Airline'] == airline)).sum()
            airlines.append(Airline(flights=flight_count, early_arrivals=dep_count, name=airline))             

        return airlines
    
if __name__ == '__main__':
    dataset_filename = "sampled_flights_data_300k.csv"
    dataset_dir = "datasets"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dataset_dir, dataset_filename)
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))

    solution = MPISolution(dataset_path=dataset_path, dataset_size=dataset_size) #total should be about 6311871
    answer, timetaken = solution.run()
