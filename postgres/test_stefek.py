import requests
import time
import numpy as np
from scipy.stats import kstest
import matplotlib.pyplot as plt
import asyncio
import aiohttp

async def send_query_async(query, url, headers):
    """Send a GraphQL query asynchronously and return the response time."""
    payload = {"query": query}
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.post(url, json=payload, headers=headers) as response:
            end_time = time.time()
            return end_time - start_time, response.status

def analyze_times(times):
    if not times:  # Check if times is empty
        print("No successful requests, cannot analyze times.")
        return
    """Calculate and print statistics about a list of times."""
    times.sort()
    numpy_times = np.asarray(times, dtype=np.float32)
    print(kstest(numpy_times, 'norm'))
    print("Average time: ", 1000*sum(times)/len(times), " ms")
    print("Variance: ", np.var(numpy_times).item()*1000, " ms")

async def run_query_stress_test(query_name, query, url, headers):
    """Run a stress test for a single query."""
    times = []
    for _ in range(10):
        response_time, status_code = await send_query_async(query, url, headers)
        if status_code == 200:
            times.append(response_time)
        else:
            print(f"Error: {status_code}")
    print("************ ", query_name, " ************")
    analyze_times(times)
    print()

graphql_queries = {  
   "gql_forms" : """
   {
        formCategoryPage {
        id
        name
        nameEn
        created
        lastchange
        }
    }"""
    ,
  "gql_ug" : """
  {
    userPage {
      id
      name
      surname
      email
      valid
    }
  }"""
}
gateway_url = "http://localhost:33000/api/gql"
headers = {"Content-Type": "application/json"}

# Run the stress test for each query
loop = asyncio.get_event_loop()
for query_name, query in graphql_queries.items():
    loop.run_until_complete(run_query_stress_test(query_name, query, gateway_url, headers))