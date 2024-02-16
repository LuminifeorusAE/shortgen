# app.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define database models
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    likes = db.Column(db.Integer)
    views = db.Column(db.Integer)
    tiktok_subscribers = db.Column(db.Integer)
    instagram_followers = db.Column(db.Integer)
    youtube_subscribers = db.Column(db.Integer)

# Routes
@app.route('/')
def index():
    videos = Video.query.all()
    # For simplicity, assuming these social network metrics are stored in the same table for now
    tiktok_subscribers = sum(video.tiktok_subscribers for video in videos)
    instagram_followers = sum(video.instagram_followers for video in videos)
    youtube_subscribers = sum(video.youtube_subscribers for video in videos)
    return render_template('index.html', videos=videos, tiktok_subscribers=tiktok_subscribers,
                           instagram_followers=instagram_followers, youtube_subscribers=youtube_subscribers)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
