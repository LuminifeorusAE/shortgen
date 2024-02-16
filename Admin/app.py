from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define database models
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    tiktok_subscribers = db.Column(db.Integer, default=0)
    instagram_followers = db.Column(db.Integer, default=0)
    youtube_subscribers = db.Column(db.Integer, default=0)

# Routes
@app.route('/videos')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        return render_template('base.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        # Save feedback to database or perform any other action
        return redirect(url_for('index'))
    return render_template('feedback.html') 

if __name__ == '__main__':
    app.run(debug=True)
