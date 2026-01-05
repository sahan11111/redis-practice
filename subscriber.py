import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

pubsub = r.pubsub()
pubsub.subscribe("user_notifications")

print("Listening for user notifications...")

for message in pubsub.listen():
    if message["type"] == "message":
        print("📢 Notification:", message["data"])
