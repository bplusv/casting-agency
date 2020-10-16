from flask import Blueprint, jsonify


bp = Blueprint('api_errors', __name__)


@bp.app_errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 400,
        'message': e.description
    }), 400


@bp.app_errorhandler(401)
def unauthorized(e):
    return jsonify({
        'success': False,
        'error': 401,
        'message': e.description
    }), 401


@bp.app_errorhandler(403)
def forbidden(e):
    return jsonify({
        'success': False,
        'error': 403,
        'message': e.description
    }), 403


@bp.app_errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': e.description
    }), 404


@bp.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        'success': False,
        'error': 405,
        'message': e.description
    }), 404


@bp.app_errorhandler(422)
def unprocessable_entity(e):
    return jsonify({
        'success': False,
        'error': 422,
        'message': e.description
    }), 422


@bp.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'success': False,
        'error': 500,
        'message': e.description
    }), 500
