from flask import Blueprint, jsonify

from application.models import Actor


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.format() for actor in actors])
