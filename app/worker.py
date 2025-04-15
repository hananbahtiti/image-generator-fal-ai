from redis import Redis
import redis
from rq import Worker, Queue
import logging

logging.basicConfig(level=logging.INFO)

# Connect to Redis
redis_conn = redis.Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)

# Define queue name
queue_name = "image_requests"

if __name__ == "__main__":
    worker = Worker([queue_name], connection=redis_conn)
    logging.info("Worker started, waiting for jobs...")
    worker.work()
