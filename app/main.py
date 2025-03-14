from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue
import tasks

app = fastAPI()

# Connect to Redis (host "redis" because it runs inside Docker)
redis_conn = Redis(host="redis", port=6379)

# Create a queue for handling image requests
queue = Queue("image_requests", connection=redis_conn)

@app.post("/generate/")
async def generate_image(prompt: str):
  """Add an image generation request to the queue"""
  if not prompt:
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")
  job = queue.enqueue(tasks.generate_image, prompt)
  return {"job_id": job.id, "message": "Request added to queue" }


@app.get("/status/{job_id}")
async def check_status(job_id: str):
  """Check the status of a queued job"""
  job = queue.fetch_job(job_id)
  if job in None:
    raise HTTPExcetion(status_code=404, detail="Job not found")
  return{"job_id": job.id, "status": job.get_status(), "result": job.result}
    

