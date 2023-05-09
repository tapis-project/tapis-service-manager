import os
from dotenv import load_dotenv


load_dotenv()

USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
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