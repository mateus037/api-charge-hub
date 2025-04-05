from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .location import Location
from .charger import Charger
from .appointment import Appointment