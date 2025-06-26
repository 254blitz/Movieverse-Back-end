import os
import requests
from flask import Blueprint, requests, jsonify
from flask_jwt_extended import jwt_required

omdb_bp = Blueprint("omdb", __name__, url_prefix="/api/movies")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@omdb_bp.route("", methods=["GET"])
@jwt_required()
def search_movies():
    search = request.args.get("search")
    if not search:
        return jsonify({"error": "Missing search parameter"}), 400

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={search}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "OMDb API request failed"}), 500

    return jsonify(response.json()), 200