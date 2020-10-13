from datetime import date

from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, abort, request

from src.models import Actor, Movie
from src.auth import requires_auth


db = SQLAlchemy()
bp = Blueprint('api_movies', __name__, url_prefix='/api')


@bp.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movie')
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    return jsonify(movie.format())


@bp.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    movies = Movie.query.all()
    if not movies:
        abort(404)
    return jsonify([movie.format() for movie in movies])


@bp.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        abort(422)


@bp.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def post_movie():
    post_data = request.get_json()
    try:
        movie = Movie(
            post_data['title'],
            date.fromisoformat(post_data['release_date'])
        )
        movie.actors = Actor.query.filter(
            Actor.id.in_(post_data.get('actors', []))).all()
        movie.insert()
        return jsonify({
            'success': True,
            'movie_id': movie.id
        })
    except Exception:
        db.session.rollback()
        abort(422)


@bp.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def patch_movie(movie_id):
    patch_data = request.get_json()
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    try:
        movie.title = patch_data['title']
        movie.release_date = date.fromisoformat(patch_data['release_date'])
        movie.actors = Actor.query.filter(
            Actor.id.in_(patch_data.get('actors', []))).all()
        movie.update()
        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        abort(422)
