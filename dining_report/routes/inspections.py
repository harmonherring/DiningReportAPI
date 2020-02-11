from flask import Blueprint, jsonify, request

from dining_report.models import Inspections

inspections_bp = Blueprint(__name__, 'inspections_bp')


@inspections_bp.route('/', methods=['GET'])
def get_inspections():
    all_inspections = Inspections.query.all()
    return jsonify({
        "status": "success",
        "data": [inspection.to_dict() for inspection in all_inspections]
    }), 200


@inspections_bp.route('/<int:location_id>', methods=['GET'])
def filtered_inspections(location_id: int):
    inspections_query = Inspections.query.\
        filter_by(location_id=location_id).all()
    if inspections_query:
        return jsonify({
            "status": "success",
            "data": [inspections.to_dict() for inspections in inspections_query]
        }), 200

    return jsonify({
        "status": "error",
        "message": "location_id doesn't exist"
    }), 404
