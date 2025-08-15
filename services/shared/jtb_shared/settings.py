import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
INIT_TOKEN = os.getenv("INIT_TOKEN", "changeme")  # used to protect /init-db and /seed-demo
