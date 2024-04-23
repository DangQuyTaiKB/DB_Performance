import requests
import json
from time import perf_counter
import asyncio

queries = {
    "rolecategories": {
        "readp": '{ result: roleCategoryPage { __typename, id, name, nameEn}}',
        "read": 'query ($id: UUID!) { result: roleCategoryById(id: $id) { __typename, id, name, nameEn }}',
        "create": '''
            mutation($id: UUID!, $name: String!, $name_en: String) {
                result: roleCategoryInsert(roleCategory: {id: $id, name: $name, nameEn: $name_en}) {
                    id
                    msg
                    result: roleCategory {
                        id
                        lastchange
                    }
                }
            }
        '''
    },

    "roletypes":{
        "readp": '{ result: roleTypePage { __typename, id, name, nameEn}}',
        "read": 'query ($id: UUID!) { result: roleTypeById(id: $id) { __typename, id, name, nameEn }}',
        "create": '''
            mutation($id: UUID!, $name: String!, $name_en: String) {
                result: roleTypeInsert(roleType: {id: $id, name: $name, nameEn: $name_en}) {
                    id
                    msg
                    result: roleType {
                        id
                        lastchange
                    }
                }
            }
        '''
    }
}

overriden_path = "http://localhost:33000/api/gql"


def execute_query(query, variables):
    body = {"query": query, "variables": variables}
    response = requests.post(overriden_path, json=body, headers={"Content-Type": "application/json"})
    result = response.json()
    return result


async def safe_fetch_page(readp):
    response = execute_query(readp, {})
    print("safeFetchPage.response", response)
    data = response.get("data")
    if data:
        print("safeFetchPage.data", data)
        result = data.get("result")
        if result:
            print("safeFetchPage.result", result)
            ids = [r["id"] for r in result]
            print("safeFetchPage", ids)
            return ids
    return []


async def run_single_test_set(readp, read):
    ids = await safe_fetch_page(readp)
    min_duration = 1000000
    max_duration = 0
    start_ticks = perf_counter()

    for identifier in ids:
        start_ticks_ = perf_counter()
        response = execute_query(read, {"id": identifier})
        duration_ = perf_counter() - start_ticks_

        max_duration = max(max_duration, duration_)
        min_duration = min(min_duration, duration_)

    duration = perf_counter() - start_ticks

    if not ids:
        return None
    else:
        return {
            "count": len(ids),
            "total": duration,
            "average": (duration / len(ids)),
            "min": min_duration,
            "max": max_duration,
        }



async def run_table_tests(on_tick):
    result = []
    for name, queryset in queries.items():
        print("runTableTests", name)
        readp, read = queryset.get("readp"), queryset.get("read")
        if readp and read:
            print("runTableTests", name)


            result_item = await run_single_test_set(readp, read)
            if result_item:
                result.append({**result_item, "query": f"{name} - by id"})
                if on_tick:
                    on_tick([{**result_item, "query": f"{name} - by id"}])


    return result


async def run_table_tests_stress(on_tick):
    result = []
    for name, queryset in queries.items():
        print("runTableTests", name)
        readp, read = queryset.get("readp"), queryset.get("read")
        if readp and read:
            print("runTableTests", name)


            idxs = list(range(10))
            promises = [run_single_test_set(readp, read) for _ in idxs]
            result_items = await asyncio.gather(*promises)
            for result_item in result_items:
                if result_item:
                    result.append({**result_item, "query": f"{name} - by id parallel"})

                    
                    if on_tick:
                        on_tick([{**result_item, "query": f"{name} - by id parallel"}])


    return result


# Define your on_tick_function here
def on_tick_function(results):
    print(results)

# Run the async functions
# result = asyncio.run(run_table_tests(on_tick_function))
# result_stress = asyncio.run(run_table_tests_stress(on_tick_function))

# result = asyncio.run(run_single_test_set(queries["rolecategories"]["readp"], queries["rolecategories"]["read"]))
result2 = asyncio.run(run_table_tests(on_tick_function))