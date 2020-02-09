from datetime import datetime

from sqlalchemy.dialects.postgresql import TEXT, DATE, BOOLEAN

from dining_report import db


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(TEXT, nullable=False)
    noncritical_violations = db.Column(db.Integer, nullable=False)
    critical_violations = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "noncritical_violations": self.noncritical_violations,
            "critical_violations": self.critical_violations
        }


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
        self.date = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
        self.noncritical_violations = noncritical_violations
        self.critical_violations = critical_violations

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "location_id": self.location_id,
            "date": str(self.date),
            "noncritical_violations": self.noncritical_violations,
            "critical_violations": self.critical_violations
        }

    def increase_critical(self):
        location = Locations.query.filter_by(id=self.location_id).first()
        location.critical_violations += 1
        self.critical_violations += 1
        db.session.commit()

    def increase_noncritical(self):
        location = Locations.query.filter_by(id=self.location_id).first()
        location.noncritical_violations += 1
        self.noncritical_violations += 1
        db.session.commit()

    @classmethod
    def create(cls, location_id, date, noncritical_violations, critical_violations):
        new_inspection = cls(location_id, date, noncritical_violations, critical_violations)
        db.session.add(new_inspection)
        db.session.commit()
        return new_inspection


class Violations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer,
                              db.ForeignKey('inspections.id'),
                              nullable=False)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('locations.id'),
                            nullable=True)
    critical = db.Column(BOOLEAN)
    data = db.Column(TEXT, nullable=False)

    def __init__(self, inspection_id: int,
                  location_id: int,
                  critical: bool,
                  data: str):
        self.inspection_id = inspection_id
        self.location_id = location_id
        self.critical = critical
        self.data = data

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "inspection_id": self.inspection_id,
            "location_id": self.location_id,
            "critical": self.critical,
            "data": self.data
        }

    @classmethod
    def create(cls, location_id, critical, data, date) -> dict:
        date_obj = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
        if not Inspections.query.filter_by(location_id=location_id, date=date_obj).first():
            inspection = Inspections.create(location_id, date, 0, 0)
        else:
            inspection = Inspections.query.filter_by(location_id=location_id, date=date).first()
        if Violations.query.filter_by(location_id=location_id, data=data, inspection_id=inspection.id).first():
            return {}
        new_violation = cls(inspection.id, location_id, critical, data)
        db.session.add(new_violation)
        db.session.commit()
        if critical:
            inspection.increase_critical()
        else:
            inspection.increase_noncritical()
        return new_violation
