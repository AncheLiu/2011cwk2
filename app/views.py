from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, case, desc
from app import app, db
from .models import User, Movie, UserMovie


@app.route('/')
def index():
    top_movies = db.session.query(Movie,
        func.count(case((UserMovie.reaction == 1, 1))).label('like_count')
        ).outerjoin(UserMovie).group_by(Movie).order_by(desc('like_count')
        ).limit(3).all()

    featured_movie_1 = top_movies[0]
    featured_movie_2 = top_movies[1]
    featured_movie_3 = top_movies[2]
    
    return render_template('base.html',
                            featured_movie_1=featured_movie_1,
                            featured_movie_2=featured_movie_2,
                            featured_movie_3=featured_movie_3,
                            movies=Movie.query.all())

#movies' id
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movies/detail.html', movie=movie)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if is_null(username, password):
            return render_template('auth/login.html', message="username and password are required")
            
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        elif exist_user(username):
            return render_template('auth/login.html', message="incorrect password")
        else:
            return render_template('auth/login.html', message="The user does not exist")
            
    return render_template('auth/login.html')

#Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            return render_template('auth/register.html', message="username and password required")
            
        elif exist_user(username):
            return render_template('auth/register.html', message="username exist")
            
        else:
            if add_user(username, password):
                # register success, go login
                return redirect(url_for('login', message="register success"))
            else:
                return render_template('auth/register.html', message="Failed to register")
            
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/movie/<int:movie_id>/react', methods=['POST'])
@login_required
def react_to_movie(movie_id):
    data = request.get_json()
    reaction_type = 1 if data.get('reaction') == 'like' else 2
    
    user_reaction = UserMovie.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if user_reaction:
        # type two times cancel
        if user_reaction.reaction == reaction_type:
            db.session.delete(user_reaction)
        # type two different update
        else:
            user_reaction.reaction = reaction_type
    else:
        user_reaction = UserMovie(
            user_id=current_user.id,
            movie_id=movie_id,
            reaction=reaction_type
        )
        db.session.add(user_reaction)
    try:
        db.session.commit()
        
        # new like and dislike number
        like_count = UserMovie.query.filter_by(
            movie_id=movie_id, 
            reaction=1
        ).count()
        dislike_count = UserMovie.query.filter_by(
            movie_id=movie_id, 
            reaction=2
        ).count()
        
        return jsonify({'status': 'success',
                        'like_count': like_count,
                        'dislike_count': dislike_count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/profile')
@login_required
def profile():
    # like number
    liked_movies = UserMovie.query.filter_by(
        user_id=current_user.id,
        reaction=1
    ).all()
    
    # dislike number
    disliked_movies = UserMovie.query.filter_by(
        user_id=current_user.id,
        reaction=2
    ).all()
    
    return render_template('user/profile.html',
                            liked_movies=liked_movies,
                            disliked_movies=disliked_movies)
#function for login
def is_null(username, password):
    return not username or not password

def is_existed(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user is not None

def exist_user(username):
    user = User.query.filter_by(username=username).first()
    return user is not None
def add_user(username, password):
    try:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        db.session.rollback()
        return False