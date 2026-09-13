
import json
import uuid

import redis
from fastapi import FastAPI


app = FastAPI()

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

@app.post("/support")
def create_support_event(message: str,  customer_id: str,):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": "support_request_created",
        "customer_id": customer_id,
        "message": message,
    }

    redis_client.rpush(
        "support_jobs",
        json.dumps(event),
    )

    return {
        "status": "accepted",
        "event_id": event["event_id"],
    }


#For idempotency, use an atomic check-and-set operation so concurrent workers cannot process the same event twice