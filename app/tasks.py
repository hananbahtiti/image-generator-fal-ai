import fal_client
from main import active_connections

def generate_image(prompt, client_id):
  """Generate an image based on the given prompt using fal-client"""
  handler = fal_client.submit(
    "fal-ai/flux-pro/v1.1",
    arguments={"prompt":prompt},
  )
  result = handler.get()
  
  # Send result to user via WebSocket if connected
  if client_id in active_connections:
    websocket = active_connections[client_id]
    websocket.send_text(f"Result: {result}")
