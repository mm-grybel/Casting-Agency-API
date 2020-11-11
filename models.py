from os import getenv
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_db(app, db_name=None):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DEV_DATABASE_URL')
    else:
        db_user = getenv('DATABASE_USER')
        db_pass = getenv('DATABASE_PASS')
        db_host = getenv('DATABASE_HOST')
        db_port = getenv('DATABASE_PORT')
        if not db_name:
            db_name = getenv('DATABASE_USER')

        app.config["SQLALCHEMY_DATABASE_URI"] = \
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    db.app = app
    db.init_app(app)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    movies = db.relationship('Movie', secondary='roles')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.format_self() for movie in self.movies]
        }

    def format_self(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f'<Actor {self.id} - {self.name}>'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_year = db.Column(db.String(4))
    genre = db.Column(db.String(50))
    actors = db.relationship('Actor', secondary='roles')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            'genre': self.genre,
            'actors': [actor.format_self() for actor in self.actors]
        }

    def format_self(self):
        return {
            'title': self.title,
            'release_year': self.release_year,
            'genre': self.genre
        }

    def __repr__(self):
        return f'<Movie {self.id} - {self.title}>'


class Role(db.Model):
    __tablename__ = 'roles'

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey('actors.id'),
        primary_key=True
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'),
        primary_key=True
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
