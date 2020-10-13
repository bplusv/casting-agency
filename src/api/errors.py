from flask import Blueprint, jsonify


bp = Blueprint('api_errors', __name__)


@bp.app_errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@bp.app_errorhandler(401)
def unauthorized(e):
    return jsonify({
        'success': False,
        'error': 401,
        'message': f'Unauthorized: {e.description}'
    }), 401


@bp.app_errorhandler(403)
def forbidden(e):
    return jsonify({
        'success': False,
        'error': 403,
        'message': f'Forbidden: {e.description}'
    }), 403


@bp.app_errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Entity not found'
    }), 404


@bp.app_errorhandler(422)
def unprocessable_entity(e):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity'
    }), 422


@bp.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500
