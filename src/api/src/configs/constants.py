import os
from dotenv import load_dotenv


load_dotenv()

SSH_USER = os.environ.get("SSH_USER")
SSH_HOST = os.environ.get("SSH_HOST")
PLATFORM = os.environ.get("PLATFORM")
IS_LOCAL = os.environ.get("IS_LOCAL", False)
SSH_SECRET_REF = os.environ.get("SSH_SECRET_REF")
SSH_TIMEOUT = os.environ.get("SSH_TIMEOUT", 300)

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