services = [
    {
        "name": "workflows",
        "base_path": "~/tapis-kube/workflows",
        "use_default_commands": True,
        "use_name_as_base_path": True,
        "allow": ["proxy"],
        "components": [
            {
                "use_default_commands": True,
                "name": "api"
            },
            {
                "use_default_commands": True,
                "name": "engine"
            }
        ]
    },
    {
        "name": "proxy",
        "base_path": "~/tapis-kube/proxy",
        "use_default_commands": True,
        "use_name_as_base_path": False,
        "components": [
            {
                "name": "nginx",
                "base_path": "nginx",
                "use_default_commands": True,
                "commands": [
                    {
                        "name": "newconfig",
                        "scripts": ["newconfig"]
                    }
                ]
            },
            {
                "name": "jupyter",
                "base_path": "jupyter",
                "use_default_commands": True,
                "commands": [
                    {
                        "name": "newhub",
                        "scripts": ["newhub"]
                    }
                ]
            }
        ]
    },
    {
        "name": "jupyterhub",
        "base_path": "~/scinco-deploy/tacc-dev.io.jupyter.tacc.cloud",
        "use_default_commands": True,
        "credentialsSecretRef": "jupyterhub-jenkins-ssh-key",
        "allow": ["workflows"],
        "components": [
            {
                "name": "jupyterhub-admin",
                "use_default_commands": True,
            },
            {
                "name": "jupyter",
                "use_default_commands": True,
            }
        ]
    }
]