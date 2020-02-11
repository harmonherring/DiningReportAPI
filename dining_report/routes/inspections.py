from flask import Blueprint, jsonify, request

from dining_report.models import Inspections

inspections_bp = Blueprint(__name__, 'inspections_bp')


@inspections_bp.route('/', methods=['GET'])
def inspections():
    if request.args.get('location_id'):
        all_inspections = Inspections.query.filter_by(location_id=request.args.get('location_id')).all()
    else:
        all_inspections = Inspections.query.all()
    return jsonify({
        "status": "success",
        "data": [inspection.to_dict() for inspection in all_inspections]
    }), 200
