from psp_auth import Auth, AuthConfig

auth = Auth(
    config=AuthConfig(
        well_known_endpoint="http://localhost:8080/v1/.well-known/openid-configuration/internal"
    )
)
