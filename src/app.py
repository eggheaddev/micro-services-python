from flask import Flask

app = Flask(__name__)

from src.routes.routes import main
app.register_blueprint(main)

def run_server():
    return app.run(port=3000, debug=True)
