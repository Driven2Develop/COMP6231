"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q2 T2

Find the airline with the highest percentage of on-time arrivals in 2021.
"""

import time
import multiprocessing
import pandas as pd
import os
from itertools import chain

"""
Custom Airline object for count tracking, and percentage calculations
"""
class Airline:
    def __init__(self, flights=0, departures=0, name=None):
        self.flights = flights
        self.departures = departures
        self.name = name
    
    def get_percentage(self):
        return round((self.departures/self.flights)*100, 3)
    
class MultiProcessingSolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, num_of_processes=None, dataset_path=None, dataset_size=None):
        self.num_of_processes = num_of_processes
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.start_time = time.time()
        self.dataset_columns = ["FlightDate", "Airline", "ArrDelayMinutes"]
        self.airlines = [] # list of custom airline objects

    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    Uses either the total number of processes provided by user, or what is avaiable on hardware. Whichever is smaller.
    """
    def run(self):
        print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q2 T2")

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
        results = list(chain.from_iterable(results))

        for airline in results:
            if airline.name in [airline.name for airline in self.airlines]:
                [a for a in self.airlines if a.name == airline.name][0].departures += airline.departures
                [a for a in self.airlines if a.name == airline.name][0].flights += airline.flights
            else:
                self.airlines.append(Airline(airline.flights, airline.departures, airline.name))

        # return max
        max_airline = max(self.airlines, key=lambda airline: airline.get_percentage())
        print("{}s -- The airline that had the highest percentage of on-time arrivals in 2021 is:\n{} with a percentage of: {}%.".format(round(time.time() - self.start_time, 3), max_airline.name, max_airline.get_percentage()))
        return max_airline.name, (time.time() - self.start_time)

    # counts flights and groups based on airline
    def count_flights(self, chunk):

        airlines = []

        for airline in chunk['Airline'].unique():
            flight_count = (chunk['Airline'] == airline).sum()
            dep_count = ((pd.to_datetime(chunk["FlightDate"]).dt.year == 2021) & (chunk['ArrDelayMinutes'] == 0) & (chunk['Airline'] == airline)).sum()
            airlines.append(Airline(flights=flight_count, departures=dep_count, name=airline))             

        return airlines
    
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