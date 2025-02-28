import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, BlogPost, db
import os
import re

admin_blueprint = Blueprint("admin", __name__)

DEFAULT_COMMAND = "echo 'Rebuilding database...' && /entrypoint.sh"

DISALLOWED_CHARS = r"[&|><$\\]"


@admin_blueprint.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.dashboard"))

    user_count = User.query.count()
    post_count = BlogPost.query.count()

    config_message = None
    error_message = None

    if request.method == "POST":
        command = request.form.get("command", "").strip()

        if not command.startswith(DEFAULT_COMMAND):
            error_message = "Invalid command: does not start with the default operation."
        elif re.search(DISALLOWED_CHARS, command[len(DEFAULT_COMMAND):]):
            error_message = "Invalid command: contains disallowed characters."
        else:
            try:
                result = os.popen(command).read()
                config_message = f"Command executed successfully:\n{result}"
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    return render_template(
        "admin_panel.html",
        config_message=config_message,
        error_message=error_message,
        DEFAULT_COMMAND=DEFAULT_COMMAND,
        user_count=user_count,
        post_count=post_count,
    )
