from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'description': 'Get current user profile',
    'security': [{'Bearer Auth': []}],
    'responses': {
        200: {
            'description': 'User profile retrieved successfully',
            'examples': {
                'application/json': {
                    'user': {
                        'id': 1,
                        'username': 'john_doe',
                        'email': 'john@example.com',
                        'created_at': '2023-10-01T12:00:00Z'
                    }
                }
            }
        },
        401: {
            'description': 'Invalid token',
            'examples': {
                'application/json': {
                    'error': 'Invalid token'
                }
            }
        }
    }
})
def get_profile():
    """
    Get User Profile Endpoint
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'description': 'Update user profile',
    'security': [{'Bearer Auth': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'new_username'},
                    'email': {'type': 'string', 'example': 'new@example.com'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Profile updated successfully',
            'examples': {
                'application/json': {
                    'message': 'Profile updated successfully',
                    'user': {
                        'id': 1,
                        'username': 'new_username',
                        'email': 'new@example.com'
                    }
                }
            }
        },
        400: {
            'description': 'Validation error',
            'examples': {
                'application/json': {
                    'error': 'Username already exists'
                }
            }
        }
    }
})
def update_profile():
    """
    Update User Profile Endpoint
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200