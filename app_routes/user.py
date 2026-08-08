from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db
from models import Trek, Booking
from forms import EditProfileForm

user_bp = Blueprint("user", __name__)


def user_required():

    if not current_user.is_authenticated:
        return False

    if not current_user.is_user():
        return False

    if current_user.blacklisted:
        return False

    return True


@user_bp.route("/dashboard")
@login_required
def dashboard():

    if not user_required():
        return redirect(url_for("auth.login"))

    treks = Trek.query.filter_by(
        status="Open"
    ).all()

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "user/dashboard.html",
        treks=treks,
        bookings=bookings
    )


@user_bp.route("/treks")
@login_required
def treks():

    if not user_required():
        return redirect(url_for("auth.login"))

    difficulty = request.args.get("difficulty")
    location = request.args.get("location")

    query = Trek.query.filter_by(status="Open")

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter(
            Trek.location.contains(location)
        )

    treks = query.all()

    return render_template(
        "user/treks.html",
        treks=treks
    )


@user_bp.route("/book/<int:id>")
@login_required
def book_trek(id):

    if not user_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    if trek.status != "Open":

        flash(
            "Bookings are closed.",
            "danger"
        )

        return redirect(
            url_for("user.treks")
        )

    if trek.available_slots <= 0:

        flash(
            "No slots available.",
            "warning"
        )

        return redirect(
            url_for("user.treks")
        )

    existing = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id
    ).first()

    if existing:

        flash(
            "You have already booked this trek.",
            "warning"
        )

        return redirect(
            url_for("user.history")
        )

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    flash(
        "Booking Successful!",
        "success"
    )

    return redirect(
        url_for("user.history")
    )


@user_bp.route("/history")
@login_required
def history():

    if not user_required():
        return redirect(url_for("auth.login"))

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/history.html",
        bookings=bookings
    )


@user_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    if not user_required():
        return redirect(url_for("auth.login"))

    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data

        db.session.commit()

        flash(
            "Profile Updated",
            "success"
        )

        return redirect(
            url_for("user.dashboard")
        )

    return render_template(
        "user/profile.html",
        form=form
    )