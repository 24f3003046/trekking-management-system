from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from forms import LoginForm, RegisterForm
from models import User
from extensions import db

auth_bp = Blueprint("auth", __name__)


# --------------------------
# Register
# --------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():

        role = form.role.data

        if role == "staff":
            approved = False
        else:
            approved = True

        user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            role=role,
            approved=approved,
            blacklisted=False
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        if role == "staff":

            flash(
                "Registration successful! Wait for Admin approval before logging in.",
                "warning"
            )

        else:

            flash(
                "Registration successful! Please login.",
                "success"
            )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html",
        form=form
    )


# --------------------------
# Login
# --------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "staff":
            return redirect(url_for("staff.dashboard"))

        return redirect(url_for("user.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user is None:

            flash(
                "Invalid username or password.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        if not user.check_password(
            form.password.data
        ):

            flash(
                "Invalid username or password.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        if user.blacklisted:

            flash(
                "Your account has been blacklisted.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if user.role == "staff" and not user.approved:

            flash(
                "Your account is awaiting Admin approval.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(user)

        flash(
            "Login successful!",
            "success"
        )

        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "staff":
            return redirect(url_for("staff.dashboard"))

        return redirect(url_for("user.dashboard"))

    return render_template(
        "login.html",
        form=form
    )


# --------------------------
# Logout
# --------------------------

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )