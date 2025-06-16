import fal_client
from redis import Redis
import logging
import os #new
from dotenv import load_dotenv #new
load_dotenv() #new

# Set the API key from environment variable
#fal_client.configure(api_key=os.getenv("FAL_API_KEY")) #new

import os
os.environ["FAL_KEY"]   ="671b3239-6a7c-4449-a85e-caa161fe3351:631d5730d85692de182d398b1b072496"

redis_conn = Redis(host="redis", port=6379)
logging.basicConfig(level=logging.INFO)

RESULT_TTL = 3600

async def generate_image(prompt, client_id):
  """Generate an image based on the given prompt using fal-client"""
  try:
    logging.info(f"Generating image for client {client_id} ...")
    handler = fal_client.submit(
      "fal-ai/flux-pro/v1.1",
      arguments={"prompt":prompt},
    )
    result = handler.get()

    redis_conn.setex(f"result: {client_id}", RESULT_TTL, result)
    logging.info(f"Image generation completed for client {client_id}")
  
  except Exception as e:
    error_msg = f"Error: {str(e)}"
    redis_conn.setex(f"result: {client_id}", RESULT_TTL, error_msg)
    logging.error(f"Failed to generate image for {client_id}: {error_msg}")
