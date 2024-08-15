import datetime
import os
import sys
time_now = datetime.datetime.now()
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Initializing the Cozo database...")
time_relative = datetime.datetime.now()
import schema
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Database Schema Done! Finished in {datetime.datetime.now() - time_relative} seconds.")
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Inserting data into the Cozo database...")
time_relative = datetime.datetime.now()
import insert_data
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Data Insertion Done! Finished in {datetime.datetime.now() - time_relative} seconds.")

print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Creating the visualization...")
time_relative = datetime.datetime.now()
import visualization
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualization Done! Finished in {datetime.datetime.now() - time_relative} seconds.")

print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Program execution completed in {datetime.datetime.now() - time_now} seconds.")
# a = (schema, insert_data, visualization)