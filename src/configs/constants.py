import os
from dotenv import load_dotenv


load_dotenv()

USER = os.environ.get("USER", "tapisdev")
HOST = os.environ.get("HOST", "cic02")
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