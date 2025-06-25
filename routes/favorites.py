from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.favorite import Favorite


favorites_bp = Blueprint('favorites_bp', __name__, url_prefix='/api/favorites')

@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    ...

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    ...
