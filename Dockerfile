# Stage 1: Build Stage
FROM python:3.7 AS build

# Copy requirements.txt to the docker image and install packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

# Set the WORKDIR to be the folder
WORKDIR /app
COPY . /app

# Stage 2: Final Stage using Distroless Image
FROM gcr.io/distroless/python3

# Set the WORKDIR to /app
WORKDIR /app

# Copy the application and installed packages from the build stage
COPY --from=build /app /app
COPY --from=build /usr/local/bin/python3.7 /usr/local/bin/python3.7
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Expose port 8080
EXPOSE 8080
ENV PORT 8080

# Use gunicorn as the entrypoint
CMD ["gunicorn", "--bind", ":$PORT", "--worker-class", "eventlet", "-w", "1", "app:app"]

