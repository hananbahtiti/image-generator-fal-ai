# Use Python as the base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy necessary files into the container
COPY requirements.txt .
COPY app /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
