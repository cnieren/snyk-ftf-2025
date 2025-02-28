from flask import Blueprint

auth_blueprint = Blueprint("auth", __name__)
blog_blueprint = Blueprint("blog", __name__)
search_blueprint = Blueprint("search", __name__)
admin_blueprint = Blueprint("admin", __name__)

from .auth import *
from .blog import *
from .search import *
from .admin import *
