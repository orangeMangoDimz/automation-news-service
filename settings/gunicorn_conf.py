import multiprocessing

# Server Socket
bind = "0.0.0.0:8000"  # Listen on all network interfaces
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal worker count
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn's async workers
timeout = 120  # Kill workers after 120 seconds of inactivity
keepalive = 5  # Keep-alive connections for 5 seconds

# Logging
loglevel = "info"

# Security
limit_request_fields = 32000  # Mitigate DDOS
limit_request_field_size = 0   # Disable unlimited header size
