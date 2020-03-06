bind = "0.0.0.0:80"

threads = 4
workers = 2
worker_class = "gthread"

# Use an in-memory filesystem to store heartbeat files
# For details, see: http://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
worker_tmp_dir = "/dev/shm"
