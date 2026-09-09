from agent import agent, critique_answer


MAX_ITERATIONS = 5
MAX_RETRIES = 2

question = "exlpalin rag, get the result length and multiplly by 2, then search for the topic in the knowledge base and return the result and finals answer multiple it by 2 and then divide by 0"


for attempt in range(MAX_RETRIES + 1):

    print(f"\n--- Attempt {attempt + 1} ---")

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ]
            },
            config={
                "recursion_limit": MAX_ITERATIONS
            },
        )

        answer = result["messages"][-1].content

        print("\nANSWER:")
        print(answer)

        critique = critique_answer(question, answer)

        print("\nCRITIQUE:")
        print(critique)

        if critique == "PASS":
            print("\nFINAL: Answer accepted.")
            break

        if attempt == MAX_RETRIES:
            print("\nFINAL: Maximum retries reached.")
            break

        print("\nRetrying agent...")

    except Exception as e:

        if "recursion" in str(e).lower():
            print("\nAGENT STOPPED:")
            print("Maximum iteration limit reached.")
            break

        raise