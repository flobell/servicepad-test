from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.database.models import User
from app.database.models import Publication