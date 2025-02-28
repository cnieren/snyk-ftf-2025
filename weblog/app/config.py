class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flaskuser:flaskpassword@localhost:3306/blog_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
