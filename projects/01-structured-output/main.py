from llm import structured_llm
from datetime import date


def extract_flight_request(message: str):
    query = f"""
    Today is {date.today()}.

    Extract the flight request from the user's message.

    If the user does not specify a year, use the next occurrence
    of that month and day in the future.

    User message:
    {message}
    """

    return structured_llm.invoke(query)

result = extract_flight_request(
    "I need to fly from Bangalore to Paris on 15th August 2027 in business class"
)
print(result)

if result.origin is None:
    print("Missing: origin")
elif result.destination is None:
    print("Missing: destination")
elif result.date is None:
    print("Missing: date")
elif result.travel_class is None:
    print("Missing: travel class")
else:
    print("Flight request is complete!")

