# main.py
from flask import Flask
from flask_cors import CORS
from routes import auth_bp  # Import the authentication routes

port = 5551

app = Flask(__name__)
CORS(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')  # All auth routes will be prefixed with /auth

if __name__ == '__main__':
    app.run(debug=True, port=port)