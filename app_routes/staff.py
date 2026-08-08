from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db
from models import Trek
from forms import StaffUpdateTrekForm

staff_bp = Blueprint("staff", __name__)


def staff_required():

    if not current_user.is_authenticated:
        return False

    if not current_user.is_staff():
        return False

    if not current_user.approved:
        return False

    if current_user.blacklisted:
        return False

    return True


@staff_bp.route("/dashboard")
@login_required
def dashboard():

    if not staff_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff/dashboard.html",
        treks=treks
    )


@staff_bp.route(
    "/trek/update/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def update_trek(id):

    if not staff_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:

        flash(
            "You are not assigned to this trek.",
            "danger"
        )

        return redirect(
            url_for("staff.dashboard")
        )

    form = StaffUpdateTrekForm(obj=trek)

    if form.validate_on_submit():

        trek.available_slots = form.available_slots.data

        trek.status = form.status.data

        db.session.commit()

        flash(
            "Trek updated successfully.",
            "success"
        )

        return redirect(
            url_for("staff.dashboard")
        )

    return render_template(
        "staff/update_trek.html",
        form=form,
        trek=trek
    )


@staff_bp.route("/participants/<int:id>")
@login_required
def participants(id):

    if not staff_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:

        flash(
            "Access Denied",
            "danger"
        )

        return redirect(
            url_for("staff.dashboard")
        )

    participants = trek.bookings

    return render_template(
        "staff/participants.html",
        trek=trek,
        participants=participants
    )