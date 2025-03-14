import fal_client

def generate_image(prompt):
  """Generate an image based on the given prompt using fal-client"""
  handler = fal_client.submit(
    "fal-ai/flux-pro/v1.1",
    arguments={"prompt":prompt},
  )
  return handler.get()
