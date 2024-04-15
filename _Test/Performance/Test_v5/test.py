
# Import necessary libraries
import requests
import json
import time
import numpy as np
import os
import docx
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import norm, expon
from statistics import mean, stdev
from io import BytesIO
import concurrent.futures


class QueryPerformanceAnalyzer:
    def __init__(self, query_file_path):
        self.query_file_path = query_file_path
        self.gateway_url = "http://localhost:33000/api/gql"
        self.headers = {"Content-Type": "application/json"}
    
    
    def runSingleTestSet(self, query, num_queries):
        times = []
        error = False

        for _ in range(num_queries):
            start_time = time.time()
            response = requests.post(self.gateway_url, json=query, headers=self.headers)
            # print(response.text)
            end_time = time.time()

            times.append((end_time - start_time) * 1000)  # Convert seconds to milliseconds

            if response.status_code != 200:
                error = True
                break

        return times, error
    



    def save_times_results(self, query, times, folder_path):
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{query}.txt")

        with open(file_path, mode='w') as file:
            for time_value in times:
                file.write(f"{time_value}\n")


    def send_queries(self, num_queries, save_file_path):
        with open(self.query_file_path, 'r') as file:
            graphql_queries = json.load(file)

        for query, graphql_query in graphql_queries.items():
            payload = {"query": graphql_query}
            times, error = self.runSingleTestSet(payload, num_queries)


            print("************ ", query, " ************")
            if error:
                print("ERROR")
                pass
            else:
                times.sort()
                numpy_times = np.asarray(times, dtype=np.float32)

                mean_val = np.mean(numpy_times).item()
                variance = np.var(numpy_times).item()
                max_val = np.max(numpy_times).item()
                min_val = np.min(numpy_times).item()
                median_val = np.median(numpy_times).item()
                stdev_val = np.std(numpy_times).item()
                percentile_90 = np.percentile(numpy_times, 90).item()


                print("Mean: ", mean_val, "ms")
                # print("Variance: ", variance)
                # print("Max: ", max_val, "ms")
                # print("Min: ", min_val, "ms")
                # print("Median: ", median_val, "ms")
                # print("Standard Deviation: ", stdev_val)
                # print("90th Percentile: ", percentile_90, "ms")

                self.save_times_results(query, times, save_file_path)

            print()



if __name__ == "__main__":
    query_file_path = 'D:/Documents/Unob_7/STC/STC_code/DB_Performance/_Test/Performance/Queries/gql_queries_test.json'
    query_analyzer = QueryPerformanceAnalyzer(query_file_path)
    query_analyzer.send_queries(1000, "results")