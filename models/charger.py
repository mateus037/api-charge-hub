from . import db

class Charger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='available', server_default='available')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    location = db.relationship('Location', backref=db.backref('chargers', lazy=True, cascade="all, delete-orphan"))

    __table_args__ = (
        db.CheckConstraint("status IN ('available', 'unavailable', 'maintenance')", name="check_status"),
    )

    def __repr__(self):
        return f'<Charger {self.id} - Status: {self.status}>'