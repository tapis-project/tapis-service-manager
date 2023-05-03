services = {
    "workflows": {
        "basePath": "~/tapis-kube/workflows",
        "useDefaultCommands": True,
        "useNameAsPath": True,
        "allow": ["proxy"],
        "components": [
            {
                "name": "api"
            },
            {
                "name": "engine"
            }
        ]
    },
    "proxy": {
        "basePath": "~/tapis-kube/proxy",
        "useDefaultCommands": True,
        "useNameAsPath": False,
        "components": [
            {
                "name": "nginx",
                "path": "nginx",
                "commands": [
                    {
                        "name": "newconfig",
                        "scripts": ["newconfig"]
                    }
                ]
            },
            {
                "name": "jupyter",
                "path": "jupyter",
                "commands": [
                    {
                        "name": "newhub",
                        "scripts": ["newhub"]
                    }
                ]
            }
        ]
    }
}