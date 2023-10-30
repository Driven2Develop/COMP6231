"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q4 T1

Find the busiest hour of the day for flights departing from "Hartsfield-Jackson Atlanta
International Airport" (ATL) in terms of the number of departures in November 2021.
"""
import time
import threading
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

class ThreadingSolution:
    """
    You are allowed to implement as many methods as you wish
    """
    def __init__(self, num_of_threads=None, dataset_path=None, dataset_size=None, dataset_columns=None):
        self.num_of_threads = num_of_threads
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.airlines = [] # list of custom airline objects
        self.start_time = time.time()
        self.dataset_columns = list(dataset_columns) # only import the columns that are necessary 
    
    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    """
    def run(self):
        threads = []
        lock = threading.Lock()
        splits = self.get_splits(self.dataset_size, self.num_of_threads) # split the dataframe into chunks for parallel processing

        # Loop for thread initialization
        for i in range(len(splits)-1):
            thread = threading.Thread(target=self.count_flights, args=(self.dataset_path, splits[i], splits[i+1], lock, i))
            threads.append(thread)
            print("{}s: Starting thread {}. Processing rows {} to {}.\n".format(round(time.time() - self.start_time, 3), i, splits[i], splits[i+1]))
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        # return max based on percentage
        max_airline = max(self.airlines, key=lambda airline: airline.get_percentage())
        return "The busiest hour of the day fro flights departing from ATL in terms of number of departures was:\n{} with a percentage of {}%.".format(max_airline.name, round(max_airline.get_percentage(), 3)), time.time() - self.start_time

    # helper method for splitting up the indexes of huge datasets depending on how many parallel mechanisms are needed
    def get_splits(self, size, num_of_splits):
        splits = []
        quotient, remainder = divmod(size, num_of_splits)
        splits = [quotient * i + min(i, remainder) for i in range(num_of_splits+1)]

        return [int(i) for i in splits] #return as a list of ints
    
    """
    Import only the data we need rows, and columns.
    Count all the flights with negative arrival times in the first 3 months of 2021
    acquire and release lock whenever interacting with the common self.airlines instance var
    """
    def count_flights(self, file_path, start_index, end_index, lock, thread_index):
        print("{}s -- Thread {} -- Loading part of CSV file from index {} to {} using pandas.\n".format(round(time.time() - self.start_time, 3), thread_index, start_index, end_index))
        df = pd.read_csv(file_path, skiprows=range(1, start_index), nrows=end_index-start_index, usecols = self.dataset_columns)
        print("{}s -- Thread {} -- Finished loading part of CSV file from index {} to {} using pandas. Processing Data.\n".format(round(time.time() - self.start_time, 3), thread_index, start_index, end_index))

        for i in range(0, end_index-start_index): # 0 index is header
            row = df.iloc[i, :]
            
            if (datetime.strptime(row["FlightDate"], "%Y-%m-%d").year == 2021 and datetime.strptime(row["FlightDate"], "%Y-%m-%d").month == 11 ):
                lock.acquire()

                # insert new entry if not in list of objects already 
                if row["Airline"] not in [airline.name for airline in self.airlines]:                
                    self.airlines.append(Airline(flights=0, early_arrivals=0, name=row["Airline"]))

                # increment departure count if criteria is met
                if row["ArrDelayMinutes"] < 0:
                    [airline for airline in self.airlines if airline.name == row["Airline"]][0].early_arrivals += 1 
                
                # always increment flight count
                [airline for airline in self.airlines if airline.name == row["Airline"]][0].flights += 1 
                
                lock.release()

        print("{}s -- Thread {} -- Data processing finished, terminating thread.\n".format(round(time.time() - self.start_time, 3), thread_index))

if __name__ == '__main__':
    print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q4 T1")
    dataset_filename = "Combined_Flights_2021_testing.csv"
    dataset_dir = "dataset"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.join(dataset_dir, dataset_filename))
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))
    dataset_columns = ["FlightDate", "Airline", "Origin"] # only import necessary columns
    num_of_threads = 30

    print("{}s: Processing flights data of size {} with {} threads.".format(round(time.time(), 3), dataset_size, num_of_threads))
    solution = ThreadingSolution(num_of_threads=num_of_threads, dataset_path=dataset_path, dataset_size=dataset_size, dataset_columns = dataset_columns) #total should be about 6311871
    answer, timetaken = solution.run()
    print("{}\nThe time it took to compute the solution was {} seconds. With {} threads.".format(answer, round(timetaken, 3), num_of_threads))