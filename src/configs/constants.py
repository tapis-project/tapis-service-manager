import os


USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
CREDENTIALS_SECRET_REF = os.environ.get("TAPIS_SERVICE_MANAGER_SECRET_NAME")

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