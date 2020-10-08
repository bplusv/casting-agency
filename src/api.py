from datetime import date

from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, abort, request

from src.models import Actor, Gender, Movie


db = SQLAlchemy()
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


@bp.route('/actors', methods=['POST'])
def post_actor():
    post_data = request.get_json()
    try:
        actor = Actor(
            post_data['name'],
            post_data['age'],
            Gender[post_data['gender'].upper()]
        ).insert()
        return jsonify({
            'success': True,
            'actor_id': actor.id
        })
    except Exception:
        db.session.rollback()
        abort(422)


@bp.route('/actors/<int:actor_id>', methods=['PATCH'])
def patch_actor(actor_id):
    patch_data = request.get_json()
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    actor.name = patch_data.get('name', actor.name)
    actor.age = patch_data.get('age', actor.age)
    actor.gender = Gender[patch_data.get('gender', actor.gender.name).upper()]
    actor.update()
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


@bp.route('/movies', methods=['POST'])
def post_movie():
    post_data = request.get_json()
    try:
        movie = Movie(
            post_data['title'],
            date.fromisoformat(post_data['release_date'])
        ).insert()
        return jsonify({
            'success': True,
            'movie_id': movie.id
        })
    except Exception:
        db.session.rollback()
        abort(422)


@bp.route('/movies/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    patch_data = request.get_json()
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.title = patch_data['title']
    movie.release_date = date.fromisoformat(patch_data['release_date'])
    movie.update()
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
