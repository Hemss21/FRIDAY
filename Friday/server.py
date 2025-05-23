from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('www', 'login.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('www', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)