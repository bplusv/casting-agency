from flask import Blueprint, jsonify, abort

from src.models import Actor, Movie


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    if not actors:
        abort(404)
    return jsonify([actor.format() for actor in actors])


@bp.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    actor.delete()
    return jsonify({
        'success': True
    })


@bp.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    if not movies:
        abort(404)
    return jsonify([movie.format() for movie in movies])


@bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.delete()
    return jsonify({
        'success': True
    })


@bp.errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@bp.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Entity not found'
    }), 404


@bp.errorhandler(422)
def unprocessable_entity(e):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity'
    }), 422


@bp.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500
