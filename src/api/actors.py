import sys

from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request, abort

from src.models import Actor, Gender, Movie
from src.auth import requires_auth


db = SQLAlchemy()
bp = Blueprint('api_actors', __name__, url_prefix='/api')


@bp.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actor')
def get_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404, description='Actor not found')
    return jsonify(actor.format())


@bp.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    actors = Actor.query.all()
    if not actors:
        abort(404, 'No Actors added yet')
    return jsonify([actor.format() for actor in actors])


@bp.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404, 'Actor not found')
    try:
        actor.delete()
        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        abort(422, 'Unprocessable request to remove Actor')


@bp.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def post_actor():
    post_data = request.get_json()
    try:
        actor = Actor(
            post_data['name'],
            post_data['age'],
            Gender[post_data['gender'].upper()]
        )
        actor.movies = Movie.query.filter(
            Movie.id.in_(post_data.get('movies', []))).all()
        actor.insert()
        return jsonify({
            'success': True,
            'actor_id': actor.id
        })
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        abort(422, 'Unprocessable request to add new Actor')


@bp.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def patch_actor(actor_id):
    patch_data = request.get_json()
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404, 'Actor not found')
    try:
        actor.name = patch_data.get('name', actor.name)
        actor.age = patch_data.get('age', actor.age)
        actor.gender = Gender[patch_data.get(
            'gender', actor.gender.name).upper()]
        actor.movies = Movie.query.filter(
            Movie.id.in_(patch_data.get('movies', []))).all()
        actor.update()
        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        abort(422, 'Unprocessable request to update existing Actor')
