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
from models import User, Trek, Booking
from forms import (
    TrekForm,
    AssignStaffForm,
    SearchForm
)

admin_bp = Blueprint("admin", __name__)

def admin_required():

    if not current_user.is_authenticated:
        return False

    return current_user.is_admin()

@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if not admin_required():
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )

@admin_bp.route("/treks")
@login_required
def manage_treks():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    if search:

        treks = Trek.query.filter(
            Trek.name.contains(search)
        ).all()

    else:

        treks = Trek.query.all()

    return render_template(
        "admin/manage_treks.html",
        treks=treks
    )

@admin_bp.route(
    "/treks/add",
    methods=["GET", "POST"]
)
@login_required
def add_trek():

    if not admin_required():
        return redirect(url_for("auth.login"))

    form = TrekForm()

    if form.validate_on_submit():

        trek = Trek(

            name=form.name.data,

            location=form.location.data,

            difficulty=form.difficulty.data,

            duration=form.duration.data,

            description=form.description.data,

            price=form.price.data,

            altitude=form.altitude.data,

            total_slots=form.total_slots.data,

            available_slots=form.available_slots.data,

            status=form.status.data,

            start_date=form.start_date.data,

            end_date=form.end_date.data
        )

        db.session.add(trek)

        db.session.commit()

        flash(
            "Trek Added Successfully",
            "success"
        )

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "admin/add_trek.html",
        form=form
    )

@admin_bp.route(
    "/treks/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_trek(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    form = TrekForm(obj=trek)

    if form.validate_on_submit():

        form.populate_obj(trek)

        db.session.commit()

        flash(
            "Trek Updated",
            "success"
        )

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "admin/edit_trek.html",
        form=form
    )

@admin_bp.route(
    "/treks/delete/<int:id>"
)
@login_required
def delete_trek(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    db.session.delete(trek)

    db.session.commit()

    flash(
        "Trek Deleted",
        "warning"
    )

    return redirect(
        url_for("admin.manage_treks")
    )

@admin_bp.route("/users")
@login_required
def manage_users():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    users = User.query.filter_by(
        role="user"
    )

    if search:

        users = users.filter(
            User.username.contains(search)
        )

    users = users.all()

    return render_template(
        "admin/manage_users.html",
        users=users
    )


@admin_bp.route("/staff")
@login_required
def manage_staff():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    staff = User.query.filter_by(
        role="staff"
    )

    if search:

        staff = staff.filter(
            User.username.contains(search)
        )

    staff = staff.all()

    return render_template(
        "admin/manage_staff.html",
        staff=staff
    )

@admin_bp.route("/staff/approve/<int:id>")
@login_required
def approve_staff(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    staff = User.query.get_or_404(id)

    staff.approved = True

    db.session.commit()

    flash(
        "Staff approved successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )

@admin_bp.route("/users/blacklist/<int:id>")
@login_required
def blacklist_user(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(id)

    user.blacklisted = True

    db.session.commit()

    flash(
        "User blacklisted.",
        "warning"
    )

    return redirect(
        url_for("admin.manage_users")
    )

@admin_bp.route("/users/unblacklist/<int:id>")
@login_required
def unblacklist_user(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(id)

    user.blacklisted = False

    db.session.commit()

    flash(
        "User restored.",
        "success"
    )

    return redirect(
        url_for("admin.manage_users")
    )

@admin_bp.route("/staff/blacklist/<int:id>")
@login_required
def blacklist_staff(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    staff = User.query.get_or_404(id)

    staff.blacklisted = True

    db.session.commit()

    flash(
        "Staff blacklisted.",
        "warning"
    )

    return redirect(
        url_for("admin.manage_staff")
    )

@admin_bp.route("/staff/unblacklist/<int:id>")
@login_required
def unblacklist_staff(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    staff = User.query.get_or_404(id)

    staff.blacklisted = False

    db.session.commit()

    flash(
        "Staff restored.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )

@admin_bp.route(
    "/treks/assign/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def assign_staff(id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    trek = Trek.query.get_or_404(id)

    form = AssignStaffForm()

    approved_staff = User.query.filter_by(
        role="staff",
        approved=True,
        blacklisted=False
    ).all()

    form.staff.choices = [
        (staff.id, staff.name)
        for staff in approved_staff
    ]

    if form.validate_on_submit():

        trek.staff_id = form.staff.data

        db.session.commit()

        flash(
            "Staff assigned successfully.",
            "success"
        )

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "admin/assign_staff.html",
        trek=trek,
        form=form
    )

@admin_bp.route("/bookings")
@login_required
def bookings():

    if not admin_required():
        return redirect(url_for("auth.login"))

    bookings = Booking.query.all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )