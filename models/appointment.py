from . import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    charger_id = db.Column(db.Integer, db.ForeignKey('charger.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='confirmed', 
                       server_default='confirmed')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('appointments', lazy=True, cascade="all, delete-orphan"))
    charger = db.relationship('Charger', backref=db.backref('appointments', lazy=True, cascade="all, delete-orphan"))

    __table_args__ = (
        db.CheckConstraint("status IN ('confirmed', 'canceled', 'done')"),
    )

    def __repr__(self):
        return f'<Appointment {self.id} - Status: {self.status}>'