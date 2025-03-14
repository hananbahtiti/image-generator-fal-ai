from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from redis import Redis
from rq import Queue
import tasks
import uuid

app = FastAPI()

# Connect to Redis (host "redis" because it runs inside Docker)
redis_conn = Redis(host="redis", port=6379, decode_responses=True)

# Create a queue for handling image requests
queue = Queue("image_requests", connection=redis_conn)

# Store active WebSocket connections
active_connections = {}

def generate_client_id():
  return str(uuid.uuid4())

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str  = None):
  """WebSocket connection to send results to users directly."""
  await websocket.accept()
  active_connections[client_id] = websocket
  try:
    while True:
      await websocket.receive_text()   # Keep connection open
  except WebSocketDisconnect:
    del active_connections[client_id]



@app.post("/generate/")
async def generate_image(prompt: str, client_id: str):
  """Add an image generation request to the queue"""
  if not prompt:
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")

  # Generate a unique client_id if not provided
  if not client_id:
    client_id = generate_client_id()
    
  # Add job to queue
  job = queue.enqueue(tasks.generate_image, prompt, client_id)
  return {"job_id": job.id, "message": "Request added to queue" }



    

