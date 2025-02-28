from flask import Blueprint, current_app, redirect, request, render_template, flash, session, url_for
from sqlalchemy import text
from models import db

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        flash("You need to log in to use the search feature.", "danger")
        return redirect(url_for('auth.login'))

    query = request.args.get("q", "")

    posts = []
    if query:
        try:
            raw_query = text(
                f"SELECT * FROM blog_posts WHERE title LIKE '%{query}%'")
            current_app.logger.info(f"Executing Raw Query: {raw_query}")
            posts = db.session.execute(raw_query).fetchall()
            current_app.logger.info(f"Query Results: {posts}")

            if not posts:
                flash("No results found for your search.", "danger")
            else:
                flash(
                    f"Found {len(posts)} results for your search.", "success")
        except Exception as e:
            current_app.logger.error(f"Query Error: {e}")
            flash(
                f"An error occurred while processing your search: {e}", "danger")
    else:
        flash("Please enter a search term.", "info")

    return render_template("search.html", posts=posts, query=query)
