# Use Python 3.7
FROM python:3.7-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\npython -c "import eventlet; eventlet.monkey_patch(); from chat.app import app, run_app; from chat import utils; utils.init_redis(); from chat.demo_data import create; import os; create() if os.environ.get('CREATE_DEMO_DATA', 'True').lower() == 'true' else None; run_app()"' > /app/start.sh \
    && chmod +x /app/start.sh

# Expose port 8000
EXPOSE 8000

# Set environment variable
ENV PORT 8000

# Use the startup script as the entrypoint
ENTRYPOINT ["/app/start.sh"]