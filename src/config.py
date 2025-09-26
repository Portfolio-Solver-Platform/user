import os


class Config:
    class App:
        NAME = "user"
        VERSION = "0.1.0"
        DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    class Api:
        TITLE = "User API"
        DESCRIPTION = "API to manage users, credentials, sessions and permissions"
        VERSION = "v1"
        ROOT_PATH = "/api/user"

    class Keycloak:
        HOST = "keycloak.keycloak.svc.cluster.local:9000"  # <svc>.<namespace>.svc.cluster.local:<port>

        class Timeout:
            DEFAULT = (1, 5)  # (connect timeout, read timeout)
            READINESS = (1, 3)
