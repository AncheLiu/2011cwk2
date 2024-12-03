import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SQLALCHEMY_DATABASE_URI
from app import app, db
from app.models import Movie, User, UserMovie

with app.app_context():
    # Replacement of previous database
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.db')):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.db'))

    db.create_all()

    # make new data
    movies = [Movie(title='Up',
                    description='''Up is a 2009 American animated comedy-drama adventure film produced 
                    by Pixar Animation Studios for Walt Disney Pictures. The film was directed by Pete Docter, 
                    co-directed by Bob Peterson, and produced by Jonas Rivera. Docter and Peterson also 
                    wrote the film's screenplay and story, with Tom McCarthy co-writing the latter. 
                    The film stars the voices of Ed Asner, Christopher Plummer, Jordan Nagai, and Bob Peterson. 
                    The film centers on Carl Fredricksen (Asner), an elderly widower who travels to South America 
                    with youngster Russell (Nagai) in order to fulfill a promise that he made to his late wife Ellie. 
                    In the jungle, they encounter an exotic bird and discover someone has sinister plans to capture it.''',
                    image_url='/static/images/up.png'),
              Movie(title='The Truman Show',
                    description='''The Truman Show is a 1998 American psychological comedy drama film
                    written and co-produced by Andrew Niccol, and directed by Peter Weir. The film depicts the story of 
                    Truman Burbank (played by Jim Carrey), a man who is unaware that he is living his entire life 
                    on a colossal soundstage, and that it is being filmed and broadcast as a reality television show 
                    which has a huge international following. All of his friends, family and members of 
                    his community are paid actors of whose job it is to sustain the illusion and keep Truman unaware 
                    about the false world he inhabits.''',
                    image_url='/static/images/The Truman Show.png'),
              Movie(title='The Shawshank Redemption',
                    description='''The Shawshank Redemption is a 1994 American prison drama film written and directed by 
                    Frank Darabont, based on the 1982 Stephen King novella Rita Hayworth and Shawshank Redemption. 
                    The film tells the story of banker Andy Dufresne (Tim Robbins), who is sentenced to life in 
                    Shawshank State Penitentiary for the murders of his wife and her lover, despite his claims of innocence. 
                    Over the following two decades, he befriends a fellow prisoner, contraband smuggler Ellis "Red" 
                    Redding (Morgan Freeman), and becomes instrumental in a money laundering operation led by the 
                    prison warden Samuel Norton (Bob Gunton). William Sadler, Clancy Brown, Gil Bellows, 
                    and James Whitmore appear in supporting roles.''',
                    image_url='/static/images/The Shawshank Redemption.png'),
              Movie(title='Interstellar',
                    description='''Interstellar is a 2014 epic science fiction drama film directed by Christopher Nolan, 
                    who co-wrote the screenplay with his brother Jonathan Nolan. It stars Matthew McConaughey, 
                    Anne Hathaway, Jessica Chastain, Bill Irwin, Ellen Burstyn, Matt Damon, and Michael Caine. 
                    Set in a dystopian future where Earth is suffering from catastrophic blight and famine, 
                    the film follows a group of astronauts who travel through a wormhole near Saturn 
                    in search of a new home for mankind.''',
                    image_url='/static/images/Interstellar.png'),
              Movie(title='Avatar',
                    description='''Avatar is a 2009 epic science fiction film co-produced, co-edited, written, 
                    and directed by James Cameron. The cast includes Sam Worthington, Zoe Saldana, 
                    Stephen Lang, Michelle Rodriguez and Sigourney Weaver. It is set in the mid-22nd century, 
                    when humans are colonizing Pandora, a lush habitable moon of a gas giant in the Alpha 
                    Centauri star system, in order to mine the valuable unobtanium, a room-temperature 
                    superconductor mineral. The expansion of the mining colony threatens the continued 
                    existence of a local tribe of Na\'vi, a humanoid species indigenous to Pandora. 
                    The title of the film refers to a genetically engineered Na\'vi body operated from 
                    the brain of a remotely located human that is used to interact with the natives 
                    of Pandora.''',
                    image_url='/static/images/Avatar.png'),
              Movie(title='Inception',
                    description='''Inception is a 2010 science fiction action heist film written and directed by Christopher Nolan, 
                    who also produced it with Emma Thomas, his wife. The film stars Leonardo DiCaprio as a professional thief 
                    who steals information by infiltrating the subconscious of his targets. He is offered a chance to have his criminal history erased 
                    as payment for the implantation of another person\'s idea into a target\'s subconscious.The ensemble cast includes Ken Watanabe, 
                    Joseph Gordon-Levitt, Marion Cotillard, Elliot Page,[a] Tom Hardy, Cillian Murphy, Tom Berenger, Dileep Rao, and Michael Caine.''',
                    image_url='/static/images/Inception.png'''),]

    # new user
    users = [User(username='11111111', password='123321'),
             User(username='22222222', password='123321'),
             User(username='33333333', password='123321')]

    # new movies
    for movie in movies:
        db.session.add(movie)
        
    for user in users:
        db.session.add(user)

    db.session.commit()

    # new comment
    user1 = User.query.filter_by(username='11111111').first()
    user2 = User.query.filter_by(username='22222222').first()
    user3 = User.query.filter_by(username='33333333').first()

    movie1 = Movie.query.filter_by(title='Avatar').first()
    movie2 = Movie.query.filter_by(title='The Shawshank Redemption').first()
    movie3 = Movie.query.filter_by(title='Interstellar').first()

    reactions = [UserMovie(user_id=user1.id, movie_id=movie1.id, reaction=1),
                 UserMovie(user_id=user1.id, movie_id=movie2.id, reaction=1),
                 UserMovie(user_id=user2.id, movie_id=movie1.id, reaction=1),
                 UserMovie(user_id=user2.id, movie_id=movie3.id, reaction=2),
                 UserMovie(user_id=user3.id, movie_id=movie1.id, reaction=2),
                 UserMovie(user_id=user3.id, movie_id=movie2.id, reaction=2),]

    # add comment
    for reaction in reactions:
        db.session.add(reaction)

    db.session.commit()