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
        HOST = "keycloak-service.keycloak.svc.cluster.local"  # <svc>.<namespace>.svc.cluster.local:<port>
        SCHEME = "http"
        PORT = 8080
        MANAGEMENT_PORT = 9000
        REALM = "master"
        CLIENT_ID = "user-service"
        CLIENT_SECRET = os.getenv(
            "KEYCLOAK_CLIENT_SECRET", "9lloVQCFgkEUfJINZ6jpasDWW13EbYcm"
        )

        class Timeout:
            DEFAULT = (1, 5)  # (connect timeout, read timeout)
            READINESS = (1, 3)
