from flask import Flask
from dotenv import load_dotenv


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Welcome to the Funemployment App!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

