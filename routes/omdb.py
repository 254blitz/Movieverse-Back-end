import os
import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.favorite import Favorite

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

    movies_data = response.json()
    if 'Search' not in movies_data:
        return jsonify([]), 200

    current_user_id = get_jwt_identity()
    user_favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    favorited_ids = {fav.movie_id for fav in user_favorites}

    # Add is_favorite flag to each movie
    for movie in movies_data['Search']:
        movie['is_favorite'] = movie.get('imdbID') in favorited_ids

    return jsonify(movies_data['Search']), 200