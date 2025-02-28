from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import BlogPost, db, User
import hashlib

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.md5(request.form.get(
            'password').encode()).hexdigest()

        user = User.query.filter_by(
            username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful!", "success")
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('login.html')


@auth_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    username = session.get('username', 'User')
    role = session.get('role', 'user')

    latest_posts = BlogPost.query.order_by(
        BlogPost.created_at.desc()).limit(5).all()

    if role == 'admin':
        return render_template('admin_dashboard.html', username=username, posts=latest_posts)
    return render_template('blog_dashboard.html', username=username, posts=latest_posts)


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = hashlib.md5(request.form.get(
            'password').encode()).hexdigest()

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already taken.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_blueprint.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        username = request.form.get('username')

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f"Password reset link sent to {user.email}.", "success")
        else:
            flash("Username not found.", "danger")

        return redirect(url_for('auth.recover'))

    return render_template('recover.html')
