from config import db, app
from models import User, Movie, Review

with app.app_context():
    print("Seeding database...")

    db.session.query(User).delete()
    db.session.query(Movie).delete()
    db.session.query(Review).delete()

    user1 = User(username="AliAbdi")
    user2 = User(username="JohnDoe")

    movie1 = Movie(title="Inception", genre="Sci-Fi")
    movie2 = Movie(title="Titanic", genre="Romance")

    review1 = Review(rating="5 Stars", user=user1, movie=movie1)
    review2 = Review(rating="4 Stars", user=user2, movie=movie2)

    db.session.add_all([user1, user2, movie1, movie2, review1, review2])
    db.session.commit()

    print("Seeding complete!")
