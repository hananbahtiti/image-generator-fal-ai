import fal_client
from redis import Redis
import logging
import os #new
from dotenv import load_dotenv #new
load_dotenv() #new

# Set the API key from environment variable
#fal_client.configure(api_key=os.getenv("FAL_API_KEY")) #new

import os
os.environ["FAL_API_KEY"]   ="9bb92bb6-5489-40e4-92a5-93ba0d8b8011:19a4171e20d14538b6bf55639c18d0f5"

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
    result = handler.get(timeout=300)

    redis_conn.setex(f"result: {client_id}", RESULT_TTL, result)
    logging.info(f"Image generation completed for client {client_id}")
  
  except Exception as e:
    error_msg = f"Error: {str(e)}"
    redis_conn.setex(f"result: {client_id}", RESULT_TTL, error_msg)
    logging.error(f"Failed to generate image for {client_id}: {error_msg}")
