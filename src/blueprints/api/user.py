from flask import Blueprint, jsonify

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def test_route():
    return jsonify(status="test")
