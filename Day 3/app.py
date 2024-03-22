from flask import Flask, jsonify, request, send_from_directory
import threading
from dotenv import load_dotenv
import os
from pdfProcessing import load_document_from_gcs, translate_to_french, similarity_to_fr_language, load_document_from_link
import requests
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, origins="http://127.0.0.1:8099", methods=["GET","POST"])
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
limiter = Limiter(get_remote_address, 
                  app=app, 
                  default_limits=["200 per hour"], 
                  storage_uri="memory://")


bucket_name = os.getenv("BUCKET_NAME")
webhook_url = os.getenv("WEBHOOK_URL")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if(password != "inipassword" or (not username)):
        return jsonify({"message": "Bad password or missing username"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token = access_token)

SWAGGER_URL = '/swagger'
API_URL = '/static/pdf_processing.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : 'My pdf processing documentation'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/", methods=["GET","PUT"])
@limiter.limit("5 per minute")
def index():
    return "Hi, This is index test", 200

@app.route("/load_document_content_from_gcs", methods=["GET","POST"])
@jwt_required()
@limiter.limit("5 per minute")
def load_document():
    try:
        data = request.get_json()
        blob = data.get("blob")
        document = threading.Thread(target=load_document_from_gcs, args=(bucket_name, blob, False))
        document.start()
        return jsonify({"success": True, "Content": "Success Loading the Document"}), 200
    except Exception as e:
        print(f"Terjadi kesalahan {e}")
        return jsonify({"success": False, "Message": "Failed to loading the Document"}), 400
  
@app.route("/load_document_content_from_link", methods=["GET","POST"])
@jwt_required()
@limiter.limit("5 per minute")
def load_document_link():
    try:
        link = request.args.get("link", default="")
        data = request.get_json()
        if(not link):
            link = data.get("link")
        if(link == ""):
            return jsonify({"success": False, "Content": "Link is missing"})
        document = threading.Thread(target=load_document_from_link, args=(link, False))
        document.start()
        return jsonify({"success": True, "Content": "Success Loading the Document"}), 200
    except Exception as e:
        print(f"Terjadi kesalahan {e}")
        return jsonify({"success": False, "Message": "Failed to loading the Document"}), 400

@app.route("/translate_text_to_french", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def translate_text_to_french():
    try:
        data = request.get_json()
        text = data.get("text")
        translated = translate_to_french(text, is_called=False)
        print(translated)
        return jsonify({"success": True, "Message": "Success translated text", "Content": translated}), 200
    except Exception as e:
        print(f"Terjadi kesalahan {e}")
        return jsonify({"success": False, "Message": "Failed to translate the text"}), 400

@app.route("/pdf_processing", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def pdf_process():
    try:
        data = request.get_json()
        platform = data.get("platform")
        if(platform not in ["link", "cloud"]):
            return jsonify({"success": False, "Content": "False platform to load the document"}), 400
        filename = ""
        if(platform == "cloud"):
            filename = data.get("filename")
            if(not filename):
                return jsonify({"success": False, "Content": "Missing argument where the platform is Cloud"}), 400
        if(platform == "link"):
            link = data.get("link")
            if(not link):
                return jsonify({"success": False, "Content": "Missing argument where the platform is Link"}), 400
        result = threading.Thread(target=similarity_to_fr_language, args=(bucket_name, filename if platform == "cloud" else link, platform))
        result.start()
        return jsonify({"success": True, "Content": "Success meload document"}), 200
    except Exception as e:
        print(f"terjadi kesalahan {e}")
        return jsonify({"success": False, "Message": "Failed to loaded document"}), 400



if __name__ == "__main__":
    print(webhook_url)
    app.run(host="localhost", debug=True, port= 1234)