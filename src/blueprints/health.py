from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/healthz")
def healthz():
    return jsonify(status="ok")


@health_bp.route("/readyz")
def readyz():
    # TODO: Check whether Keycloak is ready
    return jsonify(status="ready")
