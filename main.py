from flask import Flask
from flask_cors import CORS
from routes import auth_bp

port = 5551

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True, port=port)