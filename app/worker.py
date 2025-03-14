from redis import Redis
from rq import Worker, Queue, Connection

# Connect to Redis
redis_conn = Redis(host="redis", port=6379)

# Define queue name
queue_name = "image_requests"

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker([queue_name])
        worker.work()
