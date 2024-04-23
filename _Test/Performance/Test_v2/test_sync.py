# Import necessary libraries
import requests
import json
import time
import numpy as np
import os
import docx
import aiohttp
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
        self.headers = {"Content-Type": "application/json"}\
    
    
    def runSingleTestSet(self, query, num_queries):
        times = []
        error = False

        for _ in range(num_queries):
            start_time = time.time()
            response = requests.post(self.gateway_url, json=query, headers=self.headers)
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert seconds to milliseconds

            print(response.text)

            if response.status_code != 200:
                error = True
                break

        return times, error
    
    def send_queries(self, num_queries):
        # with open(self.query_file_path, 'r') as file:
        #     graphql_queries = json.load(file)
        
        graphql_queries = {
                "gql_roletypes" : """
                query {
                    roleTypePage {
                        id
                        name
                    }
                }"""
            }

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
                print("Mean: ", mean_val, "ms")


            print()


num_queries = 10
query_file_path = 'D:/Documents/Unob_7/STC/STC_code/DB_Performance/_Test/Performance/Queries/gql_queries_test.json'
analyzer = QueryPerformanceAnalyzer(query_file_path)
analyzer.send_queries(num_queries)




