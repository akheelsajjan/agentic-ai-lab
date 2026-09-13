import json
import time

import redis

from agent.agent import process_support_request


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

MAX_RETRIES = 3


while True:
    result = redis_client.blpop("support_jobs")

    _, job = result
    event = json.loads(job)

    print("\nReceived job:")
    print(event)

    event_id = event["event_id"]

    processing_key = f"processing:{event_id}"
    processed_key = f"processed:{event_id}"

    # Check if already successfully processed
    if redis_client.get(processed_key):
        print("Event already processed. Skipping.")
        continue

    # Claim the event
    # Temporary lock to indicate that this worker is processing the event. This prevents other workers from processing the same event simultaneously.
    claimed = redis_client.set(
        processing_key,
        "1",
        nx=True, # only set if not exists # nx=True makes sure two workers can't claim the same event simultaneously.
        ex=60, # automatically delete it after 24 hours
    )

    if not claimed:
        print("Event is already being processed. Skipping.")
        continue

    # Process with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = process_support_request(
                event["message"]
            )

            print("\nAgent response:")
            print(response)

            # Mark as successfully processed
            # This is an atomic operation that sets the processed key with a TTL of 24 hours. This ensures that even if the worker crashes after processing, the event won't be reprocessed by another worker.
            redis_client.set(
                processed_key,
                "1",
                ex=86400,
            )

            # Remove temporary processing lock
            redis_client.delete(processing_key)

            break

        except Exception as e:
            print(f"\nAttempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                time.sleep(2)

            else:
                print("Job failed after 3 attempts.")

                # Move failed event to DLQ
                redis_client.rpush(
                    "support_jobs_dlq",
                    json.dumps(event),
                )

                # Remove temporary processing lock
                redis_client.delete(processing_key)


# ------------- RETRIES --------------------------------
 
# In real systems, you usually classify errors from the HTTP status code / exception type returned by the API client,
# not by guessing from the error message.

# 200 → Success
# 400 → Bad request
# 401 → Unauthorized
# 403 → Forbidden
# 404 → Not found
# 429 → Rate limited
# 500 → Server error
# 502 → Bad gateway
# 503 → Service unavailable
# 504 → Gateway timeout

# HTTP 400
#    ↓
# Invalid request
#    ↓
# ❌ Don't retry

# HTTP 429
#    ↓
# Rate limit
#    ↓
# ✅ Retry after delay


# What happens when a job fails even after all retries? move the failed job to a Dead Letter Queue.

#A Dead Letter Queue is simply a separate queue where jobs that 
# could not be successfully processed are placed for later investigation or recovery.
# why ? You don't lose those those jobs and can inspect them to understand why they failed.

# ------------- -------------------------------------------------------------------------

# ----------------------------------------- Idempotency ------------------
#same event can be delivered more than once. Without protection, you could call the refund API twice.
# Processing the same event multiple times should produce the same final result as processing it once.
# Where is this stored? DB / or durable key-value store


#------------------------------------------------------------------------------

# NOTE
# Retry = same worker tries again because processing failed.
# Duplicate delivery = the same event arrives again, even though processing may have already succeeded.

# Important: Redis alone doesn't magically make the operation idempotent.
#  You need an atomic/check-and-set strategy and appropriate TTL/durability decisions.