import fal_client
from redis import Redis
import logging

redis_conn = Redis(host="redis", port=6379)
logging.basicConfig(level=logging.INFO)

RESULT_TTL = 3600

def generate_image(prompt, client_id):
  """Generate an image based on the given prompt using fal-client"""
  try:
    logging.info(f"Generating image for client {client_id} ...")
    handler = fal_client.submit(
      "fal-ai/flux-pro/v1.1",
      arguments={"prompt":prompt},
    )
    result = handler.get(timeout=300)

    redis_conn.setex(f"result: {client_id}", RESULT_TTL, result)
    logging.info(f"Image generation completed for client {client_id}")
  
  except Exception as e:
    error_msg = f"Error: {str(e)}"
    redis_conn.setex(f"result: {client_id}", RESULT_TTL, error_msg)
    logging.error(f"Failed to generate image for {client_id}: {error_msg}")
