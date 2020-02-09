from datetime import datetime

from sqlalchemy.dialects.postgresql import TEXT, DATE

from dining_report import db


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(TEXT, nullable=False)
    noncritical_violations = db.Column(db.Integer, nullable=False)
    critical_violations = db.Column(db.Integer, nullable=False)


class Inspections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('locations.id'),
                            nullable=False)
    date = db.Column(DATE, nullable=False)
    noncritical_violations = db.Column(db.Integer, nullable=False)
    critical_violations = db.Column(db.Integer, nullable=False)

    def __init__(self, location_id, date: str, noncritical_violations, critical_violations):
        self.location_id = location_id
        self.date = datetime.strptime(date.split('T')[0], '%y/%m/%d')
        self.noncritical_violations = noncritical_violations
        self.critical_violations = critical_violations


class Violations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer,
                              db.ForeignKey('inspections.id'),
                              nullable=False)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('locations.id'),
                            nullable=True)
    critical = db.Column(db.BOOLEAN)
    data = db.Column(TEXT, nullable=False)

    def __index__(self, inspection_id: int,
                  location_id: int,
                  critical: bool,
                  data: str):
        self.inspection_id = inspection_id
        self.location_id = location_id
        self.critical = critical
        self.data = data
