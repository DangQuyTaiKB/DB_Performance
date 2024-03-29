﻿import requests
import json
import time
import math
import numpy as np
from scipy.stats import kstest, normaltest, expon, norm
import matplotlib.pyplot as plt
import os
# import csv
# from docx import Document
# import docx


file_path = 'D:/Documents/Unob_7/STC/STC_code/DB_Performance/_Test/Performance/queries_times/gql_queries.json'
####################### send and measure queries #########################
def perform_queries(query, gateway_url, headers, payload, num_queries=100):
    times = []
    error = False

    for _ in range(num_queries):
        start_time = time.time()

        # Send the GraphQL query to the Apollo Federation gateway
        response = requests.post(gateway_url, json=payload, headers=headers)
        end_time = time.time()

        times.append((end_time - start_time) * 1000)  # Convert seconds to milliseconds

        # Check the response status
        if response.status_code != 200:
            error = True
            break

    return times, error


def save_query_times(query, times, folder_path="./queries_times"):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{query}.txt")

    with open(file_path, mode='w') as file:
        for time_value in times:
            file.write(f"{time_value}\n")

def send_queries(num_queries, save_file_path):
    with open(file_path, 'r') as file:
        graphql_queries = json.load(file)

    gateway_url = "http://localhost:33000/api/gql"
    headers = {
        "Content-Type": "application/json",
        # Add any other headers if necessary
    }

    for query, graphql_query in graphql_queries.items():
        payload = {
            "query": graphql_query,
            # You can also include variables, operationName, etc. in the payload if needed
        }

        times, error = perform_queries(query, gateway_url, headers, payload, num_queries)

        print("************ ", query, " ************")
        if error:
            print("ERROR")
            pass
        else:
            times.sort()
            numpy_times = np.asarray(times, dtype=np.float32)
            mean = np.mean(numpy_times).item()
            variance = np.var(numpy_times).item()
            print("Mean: ", mean, "ms")
            print("Variance: ", variance)

            # Save query times to CSV file
            save_query_times(query, times, save_file_path)

        print()




if __name__ == "__main__":
    num_queries = 1000
    file_path = 'D:/Documents/Unob_7/STC/STC_code/DB_Performance/_Test/Performance/queries_times/gql_queries.json'
    save_file_path = 'D:/Documents/Unob_7/STC/STC_code/DB_Performance/_Test/Performance/queries_times'
    #save_file_path = "./queries_times_postgres_single"
    #save_file_path = "./queries_times_postgres_multiple"
    #save_file_path = "./queries_times_yugabyte"
    #save_file_path = "./queries_times_cockroach"
    send_queries(num_queries, save_file_path)
    
