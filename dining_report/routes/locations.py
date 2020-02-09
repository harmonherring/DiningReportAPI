from flask import Blueprint, jsonify

from dining_report.models import Locations

location_bp = Blueprint(__name__, 'location_bp')


@location_bp.route('/', methods=['GET'])
def locations():
    all_locations = Locations.query.all()
    return jsonify({
        "status": "success",
        "data": [location.to_dict() for location in all_locations]
    }), 200


@location_bp.route('/<location_id>')
def get_location(location_id: str):
    location = Locations.query.filter_by(id=int(location_id)).first()
    if location:
        return jsonify({
            "status": "success",
            "data": location.to_dict()
        }), 200
    return jsonify({
        "status": "error",
        "message": "location does not exist"
    }), 404
