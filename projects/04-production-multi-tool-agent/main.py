# from agent.router import route_query
# from agent.orchestrator import execute_tools
# from agent.aggregator import aggregate_results

# query = "Add 2 to weather in Mumbai "

# route = route_query(query)

# print("Route:")
# for tool_call in route.tool_calls:
#     print(
#         tool_call.tool,
#         tool_call.arguments,
#         "depends_on:",
#         tool_call.depends_on,
#     )

# results = execute_tools(route)


# # print("\nFinal Answer:")
# # print(answer)
# print("\nResults:")
# for tool, result in results.items():
#     print(f"\n--- {tool} ---")
#     print(result)


# answer = aggregate_results(query, results)
# print("\nFinal Answer:")
# print(answer)



from agent.cost_router import run_with_routing


queries = [
    "What's the weather in Mumbai and calculate 25 * 4?",
]

for query in queries:
    response, metrics = run_with_routing(query)

    print(f"\nQuery: {query}")
    print("Answer:", response.content)
    print("Metrics:", metrics)