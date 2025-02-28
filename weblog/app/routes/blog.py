from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, BlogPost

blog_blueprint = Blueprint("blog", __name__)


@blog_blueprint.route("/blog", methods=["GET"])
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@blog_blueprint.route("/blog/<int:post_id>")
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("view_post.html", post=post)


@blog_blueprint.route("/blog/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        flash("Login required to create a post.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = session.get("username")

        if not title or not content:
            flash("Title and content are required.", "danger")
        else:
            new_post = BlogPost(title=title, content=content, author=author)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("blog.index"))

    return render_template("create_post.html")


@blog_blueprint.route("/blog/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if "user_id" not in session:
        flash("Login required to edit a post.", "danger")
        return redirect(url_for("auth.login"))

    post = BlogPost.query.get_or_404(post_id)
    if session.get("username") != post.author and session.get("role") != "admin":
        flash("You do not have permission to edit this post.", "danger")
        return redirect(url_for("blog.index"))

    if request.method == "POST":
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("blog.index"))

    return render_template("edit_post.html", post=post)


@blog_blueprint.route("/blog/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "user_id" not in session:
        flash("Login required to delete a post.", "danger")
        return redirect(url_for("auth.login"))

    post = BlogPost.query.get_or_404(post_id)
    if session.get("username") != post.author and session.get("role") != "admin":
        flash("You do not have permission to delete this post.", "danger")
        return redirect(url_for("blog.index"))

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("blog.index"))
