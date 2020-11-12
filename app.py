from os import getenv
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, setup_db, Actor, Movie, Role
from auth.auth import AuthError, requires_auth


def create_app(test_db=None):
    app = Flask(__name__)
    setup_db(app, test_db)
    migrate = Migrate(app, db)
    CORS(app)
    return app


APP = create_app()


'''
GET /
    It is a public endpoint.
    It returns the string "This is the Casting Agency API".
'''
@APP.route('/')
def index():
    return "This is the Casting Agency API"


# ---------- ACTOR ENDPOINTS ----------

'''
GET /actors
    It requires the 'get:actors' permission.
    It returns all actors.
'''
@APP.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in actors]

    return jsonify({
        'success': True,
        'actors': actors
    })


'''
POST /actors
    It requires the 'post:actors' permission.
    It creates a new row in the 'actors' table.
'''
@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_new_actor(payload):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    if name is None or age is None or gender is None:
        abort(400)

    try:
        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()

        return jsonify({
            'success': True,
            'actor': new_actor.format()
        })
    except Exception as e:
        print(e)
        abort(422)


'''
PATCH /actors/<actor_id>
    It requires the 'patch:actors' permission.
    It updates an actor with a given ID.
'''
@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    body = request.get_json()
    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404, description=f'Actor_id {actor_id} not found.')

    try:
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name is not None:
            actor.name = name
        if age is not None:
            actor.age = age
        if gender is not None:
            actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except Exception as e:
        print(e)
        abort(400)


'''
DELETE /actors/<actor_id>
    It requires the 'delete:actors' permission.
    It deletes an actor with a given ID.
'''
@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404, description=f'Actor_id {actor_id} not found.')

    try:
        if actor is not None:
            actor.delete()

        return jsonify({
            'success': True,
            'actor_id': actor_id
        })
    except Exception as e:
        print(e)
        abort(422)


# ---------- MOVIE ENDPOINTS ----------

'''
GET /movies
    It requires the 'get:movies' permission.
    It returns all movies.
'''
@APP.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in movies]

    return jsonify({
        'success': True,
        'movies': movies
    })


'''
POST /movies
    It requires the 'post:movies' permission.
    It creates a new row in the 'movies' table.
'''
@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_new_movie(payload):
    body = request.get_json()
    title = body.get('title', None)
    release_year = body.get('release_year', None)
    genre = body.get('genre', None)

    if title is None or release_year is None or genre is None:
        abort(400)

    try:
        new_movie = Movie(title=title, release_year=release_year, genre=genre)
        new_movie.insert()

        return jsonify({
            'success': True,
            'movie': new_movie.format()
        })
    except Exception as e:
        print(e)
        abort(422)


'''
PATCH /movies/<movie_id>
    It requires the 'patch:movies' permission.
    It updates a movie with a given ID.
'''
@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    body = request.get_json()
    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404, description=f'Movie_id {movie_id} not found.')

    try:
        title = body.get('title', None)
        release_year = body.get('release_year', None)
        genre = body.get('genre', None)

        if title is not None:
            movie.title = title
        if release_year is not None:
            movie.release_year = release_year
        if genre is not None:
            movie.genre = genre

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception as e:
        print(e)
        abort(400)


'''
DELETE /movies/<movie_id>
    It requires the 'delete:movies' permission.
    It deletes a movie with a given ID.
'''
@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404, description=f'Movie_id {movie_id} not found.')

    try:
        if movie is not None:
            movie.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id
        })
    except Exception as e:
        print(e)
        abort(422)


'''
POST /movies/<movie_id>/actors
    It requires the 'post:movies' permission.
    It ...
'''
@APP.route('/movies/<int:movie_id>/actors', methods=['POST'])
@requires_auth('post:movies')
def add_actor_to_movie(payload, movie_id):
    body = request.get_json()
    if not body or not body.get('actor_id'):
        abort(400, description='The actor_id attribute must be specified.')
    actor_id = body['actor_id']

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404, description=f'Movie_id {movie_id} not found.')

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404, description=f'Actor_id {actor_id} not found.')

    existing_role = Role.query.filter(
        (Role.movie_id == movie_id) & (Role.actor_id == actor_id))\
        .one_or_none()
    if existing_role:
        abort(409, description=f'actor_id {actor_id} \
            already has a role in movie_id {movie_id}')

    try:
        role = Role(movie_id=movie_id, actor_id=actor_id)
        role.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception as e:
        print(e)
        abort(422)


'''
DELETE /movies/<movie_id>/actors/<actor_id>
    It requires the 'delete:movies' permission.
    It ...
'''
@APP.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_actor_from_movie(payload, movie_id, actor_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404, description=f'Movie_id {movie_id} not found.')

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404, description=f'Actor_id {actor_id} not found.')

    role = Role.query.filter(
        (Role.movie_id == movie_id) &
        (Role.actor_id == actor_id)).one_or_none()
    if not role:
        abort(404, description=f'actor_id {actor_id} \
            does not have a role in movie_id {movie_id}')

    try:
        if role is not None:
            role.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id,
            'actor_id': actor_id
        })
    except Exception as e:
        print(e)
        abort(422)


# ---------- ERROR HANDLING ----------


'''
Error handlers for all expected errors including 404 and 422
'''
@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': error.description
    }), 400


@APP.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': error.description
    }), 401


@APP.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': error.description
    }), 403


@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': error.description
    }), 404

@APP.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': error.description
    }), 405


@APP.errorhandler(409)
def resource_conflict(error):
    return jsonify({
        'success': False,
        'error': 409,
        'message': error.description
    }), 409


@APP.errorhandler(422)
def unprocessable_request(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': error.description
    }), 422


@APP.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': error.description
    }), 500


'''
Error handler for AuthError
'''
@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=9000, debug=True)
