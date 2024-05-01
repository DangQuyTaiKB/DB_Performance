class QueryPerformanceAnalyzer:
    def __init__(self, query_file_path):
        self.query_file_path = query_file_path
        self.gateway_url = "http://localhost:33000/api/gql"
        self.headers = {"Content-Type": "application/json"}

    async def runSingleTestSet(self, query, num_queries):
        times = []
        error = False

        for _ in range(num_queries):
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.post(self.gateway_url, json=query, headers=self.headers) as response:
                    end_time = time.time()
                    # print(await response.text())
                    if response.status != 200:
                        error = True
                        break
                    times.append((end_time - start_time) * 1000)  # Convert seconds to milliseconds

        return times, error

    async def save_times_results(self, query, times, folder_path):
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{query}.txt")

        async with aiofiles.open(file_path, mode='w') as file:
            for time_value in times:
                await file.write(f"{time_value}\n")

    async def send_queries(self, num_queries, save_file_path):
        with open(self.query_file_path, 'r') as file:
            graphql_queries = json.load(file)

        tasks = []
        # for query, graphql_query in graphql_queries.items():
        #     payload = {"query": graphql_query}
        #     tasks.append(asyncio.create_task(self.runSingleTestSet(payload, num_queries)))

        # results = await asyncio.gather(*tasks)  # Gather results from all tasks
        # for _ in range(num_queries):
        #     payload = [{"query": graphql_query} for graphql_query in graphql_queries.values()]
        #     tasks.append(asyncio.create_task(self.runSingleTestSet(payload, 1)))

        # results = await asyncio.gather(*tasks)  # Gather results from all tasks

        query_times = {}  # Dictionary to store times for each query  //???????????????????????????
        for query, graphql_query in graphql_queries.items():
            payload = {"query": graphql_query}
            tasks.append(asyncio.create_task(self.runSingleTestSet(payload, num_queries)))

        results = await asyncio.gather(*tasks)  # Gather results from all tasks


        for query, (times, error) in zip(graphql_queries.keys(), results):
            print("************ ", query, " ************")
            if error:
                print("ERROR", query)
            else:
                query_times[query] = times #??????????????????????????
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
                # ... (print remaining statistics)

            await self.save_times_results(query, times, save_file_path)

            print()

    async def runStressTest(self, num_queries):
        with open(self.query_file_path, 'r') as file:
            graphql_queries = json.load(file)

        tasks = []
        for query, graphql_query in graphql_queries.items():
            for _ in range(num_queries):
                tasks.append(asyncio.create_task(self.runSingleTestSet({"query": graphql_query}, num_queries)))

        results = await asyncio.gather(*tasks)  # Gather results from all tasks

        return results