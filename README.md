# User Service

Service that handles user credentials, sessions and permissions.

Routes:
- `/docs` shows public API documentation.
- `/v1/.well-known/intra` gives OpenID Connect `.well-known` configuration for internal services. This endpoint uses internal cluster communication. In contrast, the public `/v1/.well-known` route provides URLs that go through the gateway.

## Usage 

Use `skaffold run -p prod` for production settings or `skaffold dev` for development settings.

## Contributing

This service is a simple proxy to [Keycloak](https://github.com/Portfolio-Solver-Platform/keycloak).

Download the development dependencies by using `pip install -r requirements-dev.txt`.

### Updating dependencies
You can manually update dependencies by:
```bash
pip-compile pyproject.toml -o requirements.txt --strip-extras
pip-compile pyproject.toml --extra dev -o requirements-dev.txt --strip-extras
```
