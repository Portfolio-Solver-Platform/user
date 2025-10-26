from psp_auth import Auth, AuthConfig, FastAPIAuth

auth = FastAPIAuth(
    Auth(
        config=AuthConfig(
            client_id="user-service",
            well_known_endpoint="http://localhost:8080/v1/.well-known/openid-configuration/internal",
        )
    ),
)
