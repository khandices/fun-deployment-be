from flask import jsonify, request
from .db import get_env, read_db, write_db
from flask import Flask
from dotenv import load_dotenv


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Welcome to the Funemployment App!"

    @app.route("/read", methods=["GET"])
    def read():
        query = f'SELECT * FROM {get_env("DB_TABLE")}'';'
        try:
            result = read_db(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/write', methods=["POST"])
    def write():
        data = request.json
        query = f'INSERT INTO {get_env("DB_TABLE")} (company_name, job_title, job_type, date_applied, location_type, referral) VALUES (%s, %s, %s, %s, %s, %s);'
        params = (data['company_name'], data['job_title'], data['job_type'], data['date_applied'],
                  data['location_type'], data['referral'])
        try:
            write_db(query, params)
            return jsonify({"message": "Data inserted successfully :)"}, 201)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

