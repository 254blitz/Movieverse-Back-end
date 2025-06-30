from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.favorite import Favorite

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add a movie to user's favorites"""
    data = request.get_json()
    
    if not data or not data.get('imdb_id') or not data.get('title'):
        return jsonify({'error': 'Missing imdb_id or title'}), 400

    current_user_id = get_jwt_identity()

    if Favorite.query.filter_by(
        user_id=current_user_id,
        movie_id=data['imdb_id']
    ).first():
        return jsonify({'error': 'Movie already in favorites'}), 409

    new_fav = Favorite(
        user_id=current_user_id,
        movie_id=data['imdb_id'],
        title=data['title'],
        poster_url=data.get('poster_url')  
    )
    
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({
        'id': new_fav.id,
        'movie_id': new_fav.movie_id,
        'title': new_fav.title,
        'poster_url': new_fav.poster_url
    }), 201

@favorites_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get all favorites for current user"""
    favorites = Favorite.query.filter_by(
        user_id=get_jwt_identity()
    ).all()

    return jsonify([{
        'id': fav.id,
        'movie_id': fav.movie_id,
        'title': fav.title,
        'poster_url': fav.poster_url
    } for fav in favorites]), 200

@favorites_bp.route('/favorites/<string:imdb_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(imdb_id):
    """Remove a movie from favorites"""
    fav = Favorite.query.filter_by(
        user_id=get_jwt_identity(),
        movie_id=imdb_id
    ).first()

    if not fav:
        return jsonify({'error': 'Favorite not found'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'message': 'Favorite removed'}), 200