from flask import Blueprint

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/dashboard")
def dashboard():
    return "Staff Dashboard"