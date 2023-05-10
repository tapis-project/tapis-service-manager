import os
from dotenv import load_dotenv


load_dotenv()

SSH_USER = os.environ.get("SSH_USER")
SSH_HOST = os.environ.get("SSH_HOST")
PLATFORM = os.environ.get("PLATFORM")
IS_LOCAL = os.environ.get("IS_LOCAL", False)
CREDENTIALS_SECRET_REF = os.environ.get("CREDENTIALS_SECRET_REF")

DEFAULT_COMMANDS = [
    {
        "name": "restart",
        "scripts": ["burndown", "burnup"]
    },
    {
        "name": "burndown",
        "scripts": ["burndown"]
    },
    {
        "name": "burnup",
        "scripts": ["burnup"]
    }
]