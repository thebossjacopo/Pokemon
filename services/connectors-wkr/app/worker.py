import time, os, sys
from datetime import datetime
from jtb_shared.db import SessionLocal
from jtb_shared import models

def run_once():
    # Placeholder: in future, call marketplace APIs and insert into listings
    print(f"[connectors] {datetime.utcnow().isoformat()} - idle (no connectors configured)")
    sys.stdout.flush()

def main():
    while True:
        run_once()
        time.sleep(300)  # sleep 5 minutes

if __name__ == "__main__":
    main()
