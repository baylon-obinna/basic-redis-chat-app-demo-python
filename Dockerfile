# Use Python 3.7
FROM python:3.7-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a Python startup script instead of a bash script
RUN echo 'import eventlet\n\
eventlet.monkey_patch()\n\
from chat.app import app, run_app\n\
from chat import utils\n\
import os\n\
\n\
utils.init_redis()\n\
\n\
if os.environ.get("CREATE_DEMO_DATA", "True").lower() == "true":\n\
    from chat.demo_data import create\n\
    create()\n\
\n\
run_app()' > /app/start.py

# Expose port 8000
EXPOSE 8000

# Set environment variable
ENV PORT 8000

# Use the Python script as the entrypoint
CMD ["python", "/app/start.py"]