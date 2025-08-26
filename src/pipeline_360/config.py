from pathlib import Path
import os

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
