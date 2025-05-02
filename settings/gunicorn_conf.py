import multiprocessing
import os

# Server Socket
bind = f"0.0.0.0:{os.getenv('GUNICORN_PORT', '8000')}" 
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal worker count
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn's async workers
timeout = 120  # Kill workers after 120 seconds of inactivity
keepalive = 5  # Keep-alive connections for 5 seconds

# Logging
loglevel = "info"

# Security
limit_request_fields = 32000  # Mitigate DDOS
limit_request_field_size = 0   # Disable unlimited header size
