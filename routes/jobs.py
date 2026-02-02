from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from ..db import LocalSession
from ..models import Job


jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    try:
        with LocalSession() as session:
            jobs = session.query(Job).all()
            result = [job.to_dict() for job in jobs]
            return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@jobs_bp.route('/jobs', methods=["POST"])
def create_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request needs to be in JSON format"}, 400)

    required_fields = [
        'company_name',
        'job_title',
        'job_type',
        'date_applied',
        'location_type',
        'referral'
    ]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        with LocalSession() as session:
            new_job = Job()
            for field, value in data.items():
                setattr(new_job, field, value)
            session.add(new_job)
            session.commit()
            session.refresh(new_job)
            return jsonify(new_job.to_dict()), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
