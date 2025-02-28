from flask import Flask, redirect, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db
from routes import auth_blueprint, blog_blueprint, search_blueprint, admin_blueprint
import logging

app = Flask(__name__)
app.config.from_object("config.Config")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler(),
    ],
)

db.init_app(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"],
)

app.register_blueprint(auth_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(admin_blueprint)


@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
