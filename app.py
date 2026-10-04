"""
K12 Hunar Scholarship Management CRM
Simple, readable Flask application for managing state scholarships.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from models import db, Scholarship, ALLOWED_STATES, ALLOWED_STATUSES
from seed import seed_database

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "k12-hunar-secret-crm")
basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, "instance")
os.makedirs(instance_dir, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(instance_dir, 'scholarships.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

_db_initialized = False

@app.before_request
def ensure_database():
    """Ensure database tables and initial seed data exist on request."""
    global _db_initialized
    if not _db_initialized:
        db.create_all()
        seed_database()
        _db_initialized = True


def validate_scholarship(data):
    """Simple server-side validation for scholarship form inputs."""
    errors = []
    name = (data.get("name") or "").strip()
    state = (data.get("state") or "").strip()
    provider_name = (data.get("provider_name") or "").strip()
    applicable_class = (data.get("applicable_class") or "").strip()
    status = (data.get("status") or "").strip()
    link = (data.get("application_link") or "").strip()

    if not name:
        errors.append("Scholarship name is required.")
    elif len(name) > 200:
        errors.append("Scholarship name must be 200 characters or fewer.")

    if not state or state not in ALLOWED_STATES:
        errors.append("Please select a valid state (Bihar, Haryana, or Jharkhand).")

    if not provider_name:
        errors.append("Provider name is required.")
    elif len(provider_name) > 200:
        errors.append("Provider name must be 200 characters or fewer.")

    if not applicable_class:
        errors.append("Applicable class is required.")
    elif len(applicable_class) > 100:
        errors.append("Applicable class must be 100 characters or fewer.")

    if not status or status not in ALLOWED_STATUSES:
        errors.append("Please select a valid status (Published, Draft, or Expired).")

    if link and not (link.startswith("http://") or link.startswith("https://")):
        errors.append("Application link must be a valid URL starting with http:// or https://")

    return errors


@app.route("/")
def dashboard():
    """Dashboard view with dynamic summary stats, filters, and scholarship list."""
    selected_state = request.args.get("state", "").strip()
    selected_status = request.args.get("status", "").strip()

    query = Scholarship.query
    if selected_state in ALLOWED_STATES:
        query = query.filter_by(state=selected_state)
    if selected_status in ALLOWED_STATUSES:
        query = query.filter_by(status=selected_status)

    scholarships = query.order_by(Scholarship.id.asc()).all()

    return render_template(
        "dashboard.html",
        scholarships=scholarships,
        total_count=Scholarship.query.count(),
        published_count=Scholarship.query.filter_by(status="Published").count(),
        draft_count=Scholarship.query.filter_by(status="Draft").count(),
        expired_count=Scholarship.query.filter_by(status="Expired").count(),
        selected_state=selected_state,
        selected_status=selected_status,
        allowed_states=ALLOWED_STATES,
        allowed_statuses=ALLOWED_STATUSES,
    )


@app.route("/scholarships/new", methods=["GET", "POST"])
def add_scholarship():
    """Add a new scholarship."""
    if request.method == "POST":
        errors = validate_scholarship(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "scholarship_form.html",
                form=request.form,
                action_title="Add Scholarship",
                button_label="Save Scholarship",
                allowed_states=ALLOWED_STATES,
                allowed_statuses=ALLOWED_STATUSES,
                is_edit=False
            ), 400

        scholarship = Scholarship(
            name=request.form["name"].strip(),
            state=request.form["state"].strip(),
            provider_name=request.form["provider_name"].strip(),
            applicable_class=request.form["applicable_class"].strip(),
            eligibility_criteria=request.form.get("eligibility_criteria", "").strip(),
            benefit=request.form.get("benefit", "").strip(),
            deadline=request.form.get("deadline", "").strip() or "Not stated",
            application_link=request.form.get("application_link", "").strip(),
            status=request.form.get("status", "Draft").strip(),
        )
        db.session.add(scholarship)
        db.session.commit()
        flash("Scholarship added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "scholarship_form.html",
        form={},
        action_title="Add Scholarship",
        button_label="Save Scholarship",
        allowed_states=ALLOWED_STATES,
        allowed_statuses=ALLOWED_STATUSES,
        is_edit=False
    )


@app.route("/scholarships/<int:id>/edit", methods=["GET", "POST"])
def edit_scholarship(id):
    """Edit an existing scholarship."""
    scholarship = db.session.get(Scholarship, id)
    if not scholarship:
        abort(404)

    if request.method == "POST":
        errors = validate_scholarship(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "scholarship_form.html",
                form=request.form,
                scholarship=scholarship,
                action_title="Edit Scholarship",
                button_label="Save Changes",
                allowed_states=ALLOWED_STATES,
                allowed_statuses=ALLOWED_STATUSES,
                is_edit=True
            ), 400

        scholarship.name = request.form["name"].strip()
        scholarship.state = request.form["state"].strip()
        scholarship.provider_name = request.form["provider_name"].strip()
        scholarship.applicable_class = request.form["applicable_class"].strip()
        scholarship.eligibility_criteria = request.form.get("eligibility_criteria", "").strip()
        scholarship.benefit = request.form.get("benefit", "").strip()
        scholarship.deadline = request.form.get("deadline", "").strip() or "Not stated"
        scholarship.application_link = request.form.get("application_link", "").strip()
        scholarship.status = request.form.get("status", scholarship.status).strip()

        db.session.commit()
        flash("Scholarship updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "scholarship_form.html",
        form=scholarship,
        scholarship=scholarship,
        action_title="Edit Scholarship",
        button_label="Save Changes",
        allowed_states=ALLOWED_STATES,
        allowed_statuses=ALLOWED_STATUSES,
        is_edit=True
    )


@app.route("/scholarships/<int:id>/status", methods=["POST"])
def update_status(id):
    """Quick inline status update from dashboard."""
    scholarship = db.session.get(Scholarship, id)
    if not scholarship:
        abort(404)

    new_status = request.form.get("status", "").strip()
    if new_status in ALLOWED_STATUSES:
        scholarship.status = new_status
        db.session.commit()
        flash("Scholarship status updated successfully.", "success")
    else:
        flash(f"Invalid status value '{new_status}'.", "danger")

    # Preserve current filter state
    redirect_state = request.form.get("current_filter_state", "")
    redirect_status = request.form.get("current_filter_status", "")
    params = {}
    if redirect_state in ALLOWED_STATES:
        params["state"] = redirect_state
    if redirect_status in ALLOWED_STATUSES:
        params["status"] = redirect_status

    return redirect(url_for("dashboard", **params))


@app.route("/scholarships/<int:id>/preview")
def preview_scholarship(id):
    """Student-facing scholarship preview."""
    scholarship = db.session.get(Scholarship, id)
    if not scholarship:
        abort(404)
    return render_template("preview.html", scholarship=scholarship)


@app.errorhandler(404)
def not_found(e):
    """404 error handler."""
    return render_template("404.html"), 404


# Auto-create tables and seed data on startup
with app.app_context():
    db.create_all()
    seed_database()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
