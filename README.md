# User Service

Service that handles user credentials, sessions and permissions.

## Contributing

This service is a simple proxy to [Keycloak](https://github.com/Portfolio-Solver-Platform/keycloak).

### Updating dependencies
You can manually update dependencies by:
```bash
pip-compile pyproject.toml -o requirements.txt --strip-extras
pip-compile pyproject.toml --extra dev -o requirements-dev.txt --strip-extras
```
