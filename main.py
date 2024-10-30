from flask import Flask
from flask_cors import CORS
from routes import auth_bp, schedule_bp, task_bp

port = 5551

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(schedule_bp, url_prefix='/schedule')
app.register_blueprint(task_bp, url_prefix='/task')

if __name__ == '__main__':
    app.run(debug=True, port=port)