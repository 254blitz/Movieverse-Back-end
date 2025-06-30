from flask import Blueprint, request, jsonify
from flask_caching import Cache
import requests
import os
from functools import wraps

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

omdb_bp = Blueprint('omdb', __name__)

def handle_omdb_errors(f):
    """Decorator to handle OMDB API errors consistently"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            api_key = os.getenv('OMDB_API_KEY')
            if not api_key:
                return jsonify({
                    "status": "error",
                    "message": "Server configuration error",
                    "code": "OMDB_KEY_MISSING"
                }), 500
                
            return f(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            return jsonify({
                "status": "error",
                "message": "Failed to connect to OMDB API",
                "details": str(e),
                "code": "NETWORK_ERROR"
            }), 502
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Internal server error",
                "code": "SERVER_ERROR"
            }), 500
    return wrapper

@omdb_bp.route('/movies', methods=['GET'])
@handle_omdb_errors
@cache.cached(timeout=3600, query_string=True)  
def search_movies():
    query = request.args.get('query')
    page = request.args.get('page', 1)
    
    if not query or not query.strip():
        return jsonify({
            "status": "error",
            "message": "Search query is required",
            "code": "INVALID_QUERY"
        }), 400
    
    omdb_url = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&s={query}&page={page}&type=movie"
    response = requests.get(omdb_url, timeout=10)  
    data = response.json()
    
    if data.get('Response') == 'False':
        return jsonify({
            "status": "error",
            "message": data.get('Error', 'OMDB API error'),
            "code": "OMDB_API_ERROR"
        }), 400 if 'Too many results' in data.get('Error', '') else 404
        
    return jsonify({
        "status": "success",
        "data": {
            'results': data.get('Search', []),
            'total': int(data.get('totalResults', 0)),
            'page': int(page)
        }
    })

@omdb_bp.route('/movies/<imdb_id>', methods=['GET'])
@handle_omdb_errors
@cache.cached(timeout=86400)  
def get_movie_details(imdb_id):
    if not imdb_id or not imdb_id.startswith('tt'):
        return jsonify({
            "status": "error",
            "message": "Invalid IMDb ID format",
            "code": "INVALID_ID"
        }), 400
    
    omdb_url = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&i={imdb_id}&plot=full"
    response = requests.get(omdb_url, timeout=10)
    data = response.json()
    
    if data.get('Response') == 'False':
        return jsonify({
            "status": "error",
            "message": data.get('Error', 'Movie not found'),
            "code": "MOVIE_NOT_FOUND"
        }), 404
        
    movie_data = {
        'title': data.get('Title'),
        'year': data.get('Year'),
        'rated': data.get('Rated'),
        'runtime': data.get('Runtime'),
        'genre': data.get('Genre'),
        'director': data.get('Director'),
        'actors': data.get('Actors'),
        'plot': data.get('Plot'),
        'poster': data.get('Poster'),
        'imdbRating': data.get('imdbRating'),
        'imdbID': data.get('imdbID')
    }
    
    return jsonify({
        "status": "success",
        "data": movie_data
    })