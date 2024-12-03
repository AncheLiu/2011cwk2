from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))

    reactions = db.relationship('UserMovie', backref='user', lazy='dynamic')

    def __repr__(self):
        return '{}{}'.format(self.id, self.username)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(100))

    reactions = db.relationship('UserMovie', backref='movie', lazy='dynamic')
    def __repr__(self):
        return '{}{}'.format(self.title, self.genre)

class UserMovie(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    reaction = db.Column(db.Integer, default=0) #0 no answer, 1 like, 2 dislike

    def __repr__(self):
        return '{}{}{}{}'.format(self.user_id, self.movie_id, self.reaction, self.is_favorite)