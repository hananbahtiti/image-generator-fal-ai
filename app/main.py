from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from redis import Redis
from rq import Queue
import tasks

app = fastAPI()

# Connect to Redis (host "redis" because it runs inside Docker)
redis_conn = Redis(host="redis", port=6379)

# Create a queue for handling image requests
queue = Queue("image_requests", connection=redis_conn)

# Store active WebSocket connections
active_connections = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, websocket_endpoint: str):
  """WebSocket connection to send results to users directly."""
  await websocket.accept()
  active_connections[client_id] = websocket
  try:
    while True
      await websocket.receive_text()   # Keep connection open
  except WebSocketDisconnect:
    del active_connections[client_id]



@app.post("/generate/")
async def generate_image(prompt: str):
  """Add an image generation request to the queue"""
  if not prompt:
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")
  job = queue.enqueue(tasks.generate_image, prompt, client_id)
  return {"job_id": job.id, "message": "Request added to queue" }



    

