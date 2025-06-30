from flask import Blueprint, request, jsonify
import requests
import os

omdb_bp = Blueprint('omdb', __name__)

@omdb_bp.route('/movies', methods=['GET'])
def search_movies():
    """Public endpoint for searching movies (no auth required)"""
    query = request.args.get('query')
    page = request.args.get('page', 1)
    
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    
    try:
        omdb_url = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&s={query}&page={page}"
        response = requests.get(omdb_url)
        data = response.json()
        
        if data.get('Response') == 'False':
            return jsonify({'error': data.get('Error', 'OMDB API error')}), 400
            
        return jsonify({
            'results': data.get('Search', []),
            'total': data.get('totalResults', 0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@omdb_bp.route('/movies/<imdb_id>', methods=['GET'])
def get_movie_details(imdb_id):
    """Public endpoint for movie details (no auth required)"""
    try:
        omdb_url = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&i={imdb_id}"
        response = requests.get(omdb_url)
        data = response.json()
        
        if data.get('Response') == 'False':
            return jsonify({'error': data.get('Error', 'Movie not found')}), 404
            
        return jsonify(data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500