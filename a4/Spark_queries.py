from functools import reduce
import os
import pandas as pd
from itertools import count, permutations
from dotenv import load_dotenv
from pyspark import RDD, SparkContext
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, avg, countDistinct
from pyspark.sql.functions import desc
from collections import Counter
from itertools import combinations

### install dependency ###
# pip install python-dotenv
# pip install pyspark # make sure you have jdk installed
#####################################

### please update your relative path while running your code ###
temp_airline_textfile = os.path.join(os.path.dirname(__file__), "flights_data.txt")
temp_airline_csvfile = os.path.join(os.path.dirname(__file__), "Combined_Flights_2021.csv")
default_spark_context = "local[*]"  # only update if you need
#######################################


### please don't update these lines ###
load_dotenv()
airline_textfile = os.getenv("AIRLINE_TXT_FILE", temp_airline_textfile)
airline_csvfile = os.getenv("AIRLINE_CSV_FILE", temp_airline_csvfile)
spark_context = os.getenv("SPARK_CONTEXT", default_spark_context)
#######################################

"""
Takes an RDD that represents the contents of the flights_data from txt file. Performs a series of MapReduce operations via PySpark
to calculate the number of co-occurring airlines with same origin airports operating on the same date, determine count of such occurrences pairwise.
Returns the results as an RDD sorted by the airline pairs alphabetically ascending (by first and then second value in the pair) with the counts in descending order.
:param flights_dat: RDD object of the contents of flights_data
:return: RDD of pairs of airline and the number of occurrences
    Example output:     [((Airline_A,Airline_B),3),
                            ((Airline_A,Airline_C),2),
                            ((Airline_B,Airline_C),1)]
"""
def co_occurring_airline_pairs_by_origin(flights_data: RDD) -> RDD:

    # Map to tuples of the form ((date, origin), airline_name) and then group by ((date, origin), [airline_name])
    # foreach (date, origin) group: count the occurrences of each airline
    # drop keys to create a dictionary of the form {airline_name, count}
    airline_count = flights_data.map(
        lambda line: tuple(line.split(','))).map(lambda x: ((x[0], x[2]), x[1])).groupByKey().mapValues(
        lambda values: dict(sorted(Counter(values).items(), key=lambda x: x[0]))
        ).values()

    # Generate pairs of airlines and group with minimum count ((airline_name1, airline_name2), min_count)
    paired_airline_count = airline_count.flatMap(
        lambda counts: (((airline1, airline2), min(count1, count2)) for (airline1, count1), (airline2, count2) in combinations(counts.items(), 2) if airline1 != airline2
    ))

    # with the pairs, add up all the counts and output in the form  ((airline_name1, airline_name2), sum) before sorting alphabetically and returning

    return paired_airline_count.reduceByKey(
        lambda count1, count2: count1 + count2).sortBy(
        lambda x: (tuple(sorted(x[0])), x[1])
    )

"""
Takes the flight data as a DataFrame and finds the airline that had the most canceled flights on Sep. 2021
:param flights: Spark DataFrame of the flights CSV file.
:return: The name of the airline with most canceled flights on Sep. 2021.
"""
def air_flights_most_canceled_flights(flights: DataFrame) -> str:

    # Create a filter and eliminate unwanted rows. Combine filters, then apply them to the Dataframe
    columns = ["Airline", "Cancelled", "Month", "Year"]
    flights.select(columns)
    filters = [
        col("Cancelled") == "TRUE",
        col("Year") == 2021,
        col("Month") == 9
    ]
    combined_filter = reduce(lambda x, y: x & y, filters) # combine filters
    airline_count = flights.filter(combined_filter) # apply filter

    # get airline counts and return the one with highest frequency
    return airline_count.groupBy("Airline").count().orderBy(col("count").desc()).select("Airline").collect()[0][0] 

    """
    Takes the flight data as a DataFrame and calculates the number of flights that were diverted in the period of
    20-30 Nov. 2021.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The number of diverted flights between 20-30 Nov. 2021.
    """
def air_flights_diverted_flights(flights: DataFrame) -> int:
    
    # Create a filter and eliminate unwanted rows. Combine filters, then apply them to the Dataframe
    columns = ["Diverted", "DayOfMonth", "Month", "Year"]
    flights.select(columns)
    filters = [
        col("Month") == 11,
        col("Year") == 2021,
        col("Diverted") == "TRUE",
        (col("DayOfMonth") >= 20) & (col("DayOfMonth") <= 30)
    ]

    combined_filter = reduce(lambda x, y: x & y, filters)
    airline_count = flights.filter(combined_filter)

    # return the total count
    return airline_count.count()

    """
    Takes the flight data as a DataFrame and calculates the average airtime of the flights from Nashville, TN to
    Chicago, IL.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The average airtime average airtime of the flights from Nashville, TN to
    Chicago, IL.
    """
def air_flights_avg_airtime(flights: DataFrame) -> float:
    
    # Create a filter and eliminate unwanted rows. Combine filters, then apply them to the Dataframe
    columns = ["OriginCityName", "DestCityName", "AirTime"]
    flights.select(columns)
    filters = [
        col("OriginCityName") == "Nashville, TN",
        col("DestCityName") == "Chicago, IL"
    ]

    combined_filter = reduce(lambda x, y: x & y, filters)
    airline_count = flights.filter(combined_filter)

    # return the average of airtimes
    return airline_count.agg(avg(col("AirTime")).alias("AverageAirTime")).collect()[0]["AverageAirTime"]

    """
    Takes the flight data as a DataFrame and find the number of unique dates where the departure time (DepTime) is
    missing.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: the number of unique dates where DepTime is missing.
    """
def air_flights_missing_departure_time(flights: DataFrame) -> int:

    # Create a filter and eliminate unwanted rows. Combine filters, then apply them to the Dataframe
    columns = ["FlightDate", "DepTime"]
    flights.select(columns)
    filters = [
        col("DepTime").isNull() | (col("DepTime") == "None")
    ]

    combined_filter = reduce(lambda x, y: x & y, filters)
    airline_count = flights.filter(combined_filter)

    # return the unique flight dates.
    return airline_count.agg(countDistinct("FlightDate").alias("UniqueFlightDates")).collect()[0]["UniqueFlightDates"]

def main():
    # initialize SparkContext and SparkSession
    sc = SparkContext(spark_context)
    spark = SparkSession.builder.getOrCreate()

    print("########################## Problem 1 ########################")
    # problem 1: co-occurring operating flights with Spark and MapReduce
    # read the file
    flights_data = sc.textFile(airline_textfile)
    sorted_airline_pairs = co_occurring_airline_pairs_by_origin(flights_data)
    sorted_airline_pairs.persist()
    for pair, count in sorted_airline_pairs.take(10):
        print(f"{pair}: {count}")

    print("########################## Problem 2 ########################")
    # problem 2: PySpark DataFrame operations
    # read the file
    flights = spark.read.csv(airline_csvfile, header=True, inferSchema=True)
    print(
        "Q1:",
        air_flights_most_canceled_flights(flights),
        "had the most canceled flights in September 2021.",
    )
    print(
        "Q2:",
        air_flights_diverted_flights(flights),
        "flights were diverted between the period of 20th-30th " "November 2021.",
    )
    print(
        "Q3:",
        air_flights_avg_airtime(flights),
        "is the average airtime for flights that were flying from "
        "Nashville to Chicago.",
    )
    print(
        "Q4:",
        air_flights_missing_departure_time(flights),
        "unique dates where departure time (DepTime) was " "not recorded.",
    )


if __name__ == "__main__":
    main()
