"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q4 T2

Find the busiest hour of the day for flights departing from "Hartsfield-Jackson Atlanta
International Airport" (ATL) in terms of the number of departures in November 2021.
"""

import time
import multiprocessing
import pandas as pd
import os
from datetime import datetime

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
    
class MultiProcessingSolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, num_of_processes=None, dataset_path=None, dataset_size=None, dataset_columns=None):
        self.num_of_processes = num_of_processes
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.start_time = time.time()
        self.dataset_columns = list(dataset_columns)
        self.airlines = [] # list of custom airline objects

    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    Uses either the total number of processes provided by user, or what is avaiable on hardware. Whichever is smaller.
    """
    def run(self):
        splits = self.get_splits(self.dataset_size, min(multiprocessing.cpu_count(), self.num_of_processes))

        manager = multiprocessing.Manager().list()
        processes = []

        # Loop for process initialization
        for i in range(len(splits)-1):
            p = multiprocessing.Process(target=self.count_flights, args=(self.dataset_path, splits[i], splits[i+1], manager, i))
            processes.append(p)
            print("{}s: Starting process {}. Processing rows {} to {}.\n".format(round(time.time() - self.start_time, 3), i, splits[i], splits[i+1]))
            p.start()
        
        # Wait for all processes to finish, then close them
        for process in processes:
            process.join()
        
        for process in processes:
            process.close()
        
        # use manager to combine results from processes
        for airline in manager:
            if airline.name in [airline.name for airline in self.airlines]:
                found = [aline for aline in self.airlines if aline.name == airline.name][0]
                found.flights += airline.flights
                found.early_arrivals += airline.early_arrivals
            else:
                self.airlines.append(airline)
        
        #get max
        max_airline = max(self.airlines, key=lambda airline: airline.get_percentage())
        return "The airline that had the highest percentage of early arrivals in the first quarter (January, February, March) of 2021 is:\n{} with a percentage of {}%.".format(max_airline.name, round(max_airline.get_percentage(), 3)), time.time() - self.start_time

    """  
    Import only the data we need rows, and columns.
    Count all the flights with negative arrival times in the first 3 months of 2021
    acquire and release lock whenever interacting with the common self.airlines instance var
    """
    def count_flights(self, file_path, start_index, end_index, manager, process_index):
        print("{}s -- Process {} -- Loading part of CSV file from index {} to {} using pandas.\n".format(round(time.time() - self.start_time, 3), process_index, start_index, end_index))
        df = pd.read_csv(file_path, skiprows=range(1, start_index), nrows=end_index-start_index, usecols = self.dataset_columns)
        print("{}s -- Process {} -- Loading part of CSV file from index {} to {} using pandas.\n".format(round(time.time() - self.start_time, 3), process_index, start_index, end_index))

        airlines = [] #list of custom airline objects

        for i in range(1, len(df)): # 0 index is header
            row = df.iloc[i, :]

            if (datetime.strptime(row["FlightDate"], "%Y-%m-%d").year == 2021 and datetime.strptime(row["FlightDate"], "%Y-%m-%d").month == 11 ):

                # insert new entry if not in list of objects already
                if row["Airline"] not in [airline.name for airline in airlines]: 
                    airlines.append(Airline(flights=0, early_arrivals=0, name=row["Airline"]))
                
                # increment departure count if criteria is met
                if row["ArrDelayMinutes"] < 0:
                    [airline for airline in airlines if airline.name == row["Airline"]][0].early_arrivals += 1
                
                # always increment flight count
                [airline for airline in airlines if airline.name == row["Airline"]][0].flights += 1

        manager.extend(airlines)
        print("{}s -- Process {} -- Data processing finished, terminating Process.\n".format(round(time.time() - self.start_time, 3), process_index))


    # helper method for splitting up the indexes of huge datasets depending on how many parallel mechanisms are needed
    def get_splits(self, size, num_of_splits):
        splits = []
        quotient, remainder = divmod(size, num_of_splits)
        splits = [quotient * i + min(i, remainder) for i in range(num_of_splits+1)]

        return [int(i) for i in splits] #return as a list of ints

if __name__ == '__main__':
    print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T2")
    dataset_filename = "Combined_Flights_2021_testing.csv"
    dataset_dir = "dataset"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.join(dataset_dir, dataset_filename))
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))
    dataset_columns = ["FlightDate", "Airline", "Origin"] # only import necessary columns
    num_of_processes = 4

    print("Processing flights data of size {} with {} processes.".format(dataset_size, num_of_processes))
    solution = MultiProcessingSolution(num_of_processes=num_of_processes, dataset_path=dataset_path, dataset_size=dataset_size, dataset_columns=dataset_columns)
    answer, timetaken = solution.run()
    print("{}\nThe time it took to compute the solution was {} seconds. With {} threads.".format(answer, round(timetaken, 3), num_of_processes))