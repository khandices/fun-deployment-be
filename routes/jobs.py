from flask import Blueprint, jsonify, request
from ..db import get_env, read_db, write_db


jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    query = f'SELECT * FROM {get_env("jobs")};'
    try:
        result = read_db(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jobs_bp.route('/jobs', methods=["POST"])
def create_job():
    data = request.json
    query = f'INSERT INTO {get_env("jobs")} (company_name, job_title, job_type, date_applied, location_type, referral) VALUES (%s, %s, %s, %s, %s, %s);'
    params = (
        data['company_name'],
        data['job_title'],
        data['job_type'],
        data['date_applied'],
        data['location_type'],
        data['referral']
    )

    try:
        write_db(query, params)
        return jsonify({"message": "Job creation successful :)"}, 201)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
