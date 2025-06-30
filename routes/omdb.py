from flask import Blueprint, request, jsonify
from flask_caching import Cache
import requests
import os
from functools import wraps

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

omdb_bp = Blueprint('omdb', __name__)
OMDB_BASE_URL = "http://www.omdbapi.com/"

def handle_omdb_errors(f):
    """Decorator for consistent OMDB API error handling"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            api_key = os.getenv('OMDB_API_KEY')
            if not api_key:
                return jsonify({
                    "status": "error",
                    "message": "OMDB API key not configured",
                    "code": "CONFIG_ERROR"
                }), 500
            return f(*args, **kwargs)
        except requests.exceptions.Timeout:
            return jsonify({
                "status": "error",
                "message": "OMDB API timeout",
                "code": "TIMEOUT"
            }), 504
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
    """
    Search movies by title
    Parameters:
        query (required): Search term
        page (optional): Results page number
    """
    query = request.args.get('query', '').strip()
    page = request.args.get('page', '1')
    
    if not query:
        return jsonify({
            "status": "error",
            "message": "Search query is required",
            "code": "INVALID_QUERY"
        }), 400
    
    try:
        page = int(page)
        if page < 1:
            raise ValueError
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Page must be a positive integer",
            "code": "INVALID_PAGE"
        }), 400

    params = {
        'apikey': os.getenv('OMDB_API_KEY'),
        's': query,
        'page': page,
        'type': 'movie'
    }
    
    response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
    data = response.json()
    
    if data.get('Response') == 'False':
        error_msg = data.get('Error', 'Unknown OMDB API error')
        status_code = 400 if 'Too many results' in error_msg else 404
        return jsonify({
            "status": "error",
            "message": error_msg,
            "code": "OMDB_ERROR"
        }), status_code
        
    return jsonify({
        "status": "success",
        "data": {
            'results': data.get('Search', []),
            'total_results': int(data.get('totalResults', 0)),
            'page': page
        }
    })

@omdb_bp.route('/movies/<imdb_id>', methods=['GET'])
@handle_omdb_errors
@cache.cached(timeout=86400)  
def get_movie_details(imdb_id):
    """
    Get detailed movie information by IMDb ID
    Parameters:
        imdb_id (required): IMDb ID (must start with 'tt')
    """
    if not imdb_id or not imdb_id.startswith('tt'):
        return jsonify({
            "status": "error",
            "message": "Invalid IMDb ID format - must start with 'tt'",
            "code": "INVALID_ID"
        }), 400
    
    params = {
        'apikey': os.getenv('OMDB_API_KEY'),
        'i': imdb_id,
        'plot': 'full'  
    }
    
    response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
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
        'imdb_rating': data.get('imdbRating'),
        'imdb_id': data.get('imdbID'),
        'type': data.get('Type')
    }
    
    return jsonify({
        "status": "success",
        "data": movie_data
    })