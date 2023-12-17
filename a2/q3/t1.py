"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.

Q3 T1

Find the airline that had the highest percentage of flights arriving early (with a
negative arrival delay) in the first quarter of 2021.
"""

import time
import threading
import pandas as pd
import os

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
    def __init__(self, num_of_threads=None, dataset_path=None, dataset_size=None):
        self.num_of_threads = num_of_threads
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size
        self.airlines = [] # list of custom airline objects
        self.start_time = time.time()
        self.dataset_columns = ["FlightDate", "Airline", "ArrDelay"]  # only import the columns that are necessary 
    
    """
    Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
    """
    def run(self):
        print("Iymen Abdella | 40218280 | COMP 6231 FALL 2023 | Assignment 2: Parallel Programming | Q3 T1")
        threads = []
        lock = threading.Lock()

        # load csv and filter based on acceptance criteria
        print("{}s -- Loading csv file, and filtering based on acceptance criteria.".format(round(time.time() - self.start_time, 3)))
        df = pd.read_csv(self.dataset_path, usecols = self.dataset_columns)
        filtered_df = self.filter_csv(df)
        print("{}s -- Dataframe loaded.".format(round(time.time() - self.start_time, 3)))

        # find all the unique airlines and initialize them as custom objects
        print("{}s -- Finding all unique airline names.".format(round(time.time() - self.start_time, 3)))

        for airline in df['Airline'].unique():
            flight_count = (df['Airline'] == airline).sum()
            self.airlines.append(Airline(flights=flight_count, early_arrivals=0, name=airline))
        
        print("{}s -- All unique airline names found.".format(round(time.time() - self.start_time, 3)))

        splits = self.get_splits(len(filtered_df), self.num_of_threads) # split the filtered dataframe into chunks for parallel processing
        
        # thread initialization loop
        for i in range(len(splits)-1):
            thread = threading.Thread(target=self.count_flights, args=(filtered_df, splits[i], splits[i+1], lock, i))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        # return max based on percentage
        max_airline = max(self.airlines, key=lambda airline: airline.get_percentage())
        print("{}s -- The airline that had the highest percentage of early arrivals in the first quarter of 2021 is :\n{} with a percentage of: {}%.".format(round(time.time() - self.start_time, 3), max_airline.name, max_airline.get_percentage()))

        return max_airline.name, (time.time() - self.start_time)
    
    # helper method to filter out flights based on acceptance criteria reducing the counting effort
    def filter_csv(self, df):
        start_date = pd.to_datetime('2021-01-01')
        end_date = pd.to_datetime('2021-03-31')
        filter = (pd.to_datetime(df["FlightDate"]) >= start_date) & (pd.to_datetime(df["FlightDate"]) <= end_date) & (df['ArrDelay'] < 0)  
        return df[filter]
    
    # helper method for splitting up the indexes of huge datasets depending on how many parallel mechanisms are needed
    def get_splits(self, size, num_of_splits):
        splits = []
        quotient, remainder = divmod(size, num_of_splits)
        splits = [quotient * i + min(i, remainder) for i in range(num_of_splits+1)]

        return [int(i) for i in splits] #return as a list of ints
    
    # counts flights and groups based on airline
    def count_flights(self, df, start_index, end_index, lock, thread_index):
        print("{}s -- Thread: {} -- Processing part of filtered CSV file from index {} to {}.\n".format(round(time.time() - self.start_time, 3), thread_index, start_index, end_index))

        for i in range(start_index, end_index): # 0 index is header
            row = df.iloc[i, :]
            lock.acquire()
            [airline for airline in self.airlines if airline.name == row["Airline"]][0].early_arrivals += 1 
            lock.release()
        
        print("{}s -- Thread: {} -- Processing finished, terminating thread.\n".format(round(time.time() - self.start_time, 3), thread_index))

if __name__ == '__main__':
    dataset_filename = "Combined_Flights_2021.csv"
    dataset_dir = "dataset"
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.join(dataset_dir, dataset_filename))
    dataset_size = len(pd.read_csv(dataset_path, usecols=["FlightDate"]))
    num_of_threads = 4

    print("{}s: Processing flights data of size {} with {} threads.".format(round(time.time(), 3), dataset_size, num_of_threads))
    solution = ThreadingSolution(num_of_threads=num_of_threads, dataset_path=dataset_path, dataset_size=dataset_size) #total should be about 6311871
    answer, timetaken = solution.run()
    print("The time it took to compute the solution was {} seconds. With {} threads.".format(round(timetaken, 3), num_of_threads))