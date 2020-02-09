from flask import Blueprint, jsonify

from dining_report import socrata_client, app
from dining_report.models import Locations, Violations

populate_bp = Blueprint(__name__, 'populate_bp')


@populate_bp.route('/')
def populate():
    locations = Locations.query.all()
    for location in locations:
        print(location.id)
        violations = socrata_client.get(app.config['SOCRATA_DATASET_ID'],
                                        limit=420000,
                                        facility_code=str(location.id) + " ")
        for violation in violations:
            date_of_inspection = violation.get('date_of_inspection')
            facility_code = violation.get('facility_code')
            violation_description = violation.get('violation_description')
            critical_violation = violation.get('critical_violation')

            if date_of_inspection and facility_code and violation_description and critical_violation:
                critical= 1 if critical_violation == "Critical Violation" else 0
                Violations.create(facility_code, critical, violation_description, date_of_inspection)
    return '', 204
