"""
Gunicorn Configuration for FNCS API Production Deployment
Optimized for Render.com free tier
"""

import os
import multiprocessing

# Server Socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
backlog = 2048

# Worker Processes
workers = 2
worker_class = 'sync'
worker_connections = 1000
threads = 4
timeout = 120
keepalive = 5

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process Naming
proc_name = 'fncs-api'

# Server Hooks
def on_starting(server):
    """
    Called just before the master process is initialized
    """
    print("=" * 80)
    print("FNCS API Starting on Render.com")
    print("=" * 80)

def on_reload(server):
    """
    Called to recycle workers during a reload via SIGHUP
    """
    print("Reloading FNCS API workers...")

def when_ready(server):
    """
    Called just after the server is started
    """
    print(f"FNCS API is ready. Listening on {bind}")
    print("=" * 80)

def on_exit(server):
    """
    Called just before exiting
    """
    print("FNCS API shutting down...")
