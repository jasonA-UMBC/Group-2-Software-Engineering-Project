import os

token = os.environ.get("GH_TOKEN")
if not token:
    raise ValueError("GH_TOKEN environment variable is not set.")