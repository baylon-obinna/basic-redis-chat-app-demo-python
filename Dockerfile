# Use Python 3.7
FROM python:3.7-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Set environment variable
ENV PORT 8000

# Use gunicorn as the entrypoint
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "--worker-class", "eventlet", "-w", "1", "app:app"]