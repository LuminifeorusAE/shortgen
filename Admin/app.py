from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from OAuth_autorization import generate_title_and_description
import subprocess
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for flash messages
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

# Function to delete the generated video file
def delete_video_file(file_name: str):
    try:
        os.remove(file_name)
        print(f"Deleted video file: {file_name}")
    except FileNotFoundError:
        print(f"Video file {file_name} not found.")
    except Exception as e:
        print(f"An error occurred while deleting the video file: {e}")


def create_video():
    try:
        # Generate title and description
        title, description = generate_title_and_description()
        
        # Create new video object
        video = Video(title=title, description=description)
        db.session.add(video)
        db.session.commit()
        
        # Replace 'bot_1_0_2.py' with the actual name of your video creation script
        subprocess.run(["python", "bot_1_0_2.py"], check=True)
        flash('Video created successfully!', 'success')
    except Exception as e:
        flash(f'Error creating video: {e}', 'error')

# Routes
@app.route('/index')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)


@app.route('/delete/<int:video_id>', methods=['POST'])
def delete(video_id):
    # Retrieve the video object from the database
    video = Video.query.get_or_404(video_id)
    
    # Delete the video file (assuming the file name is stored in the video object)
    delete_video_file(video.file_name)
    
    # Delete the video object from the database
    db.session.delete(video)
    db.session.commit()
    
    flash('Video deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/create_video', methods=['POST'])
def create_video_route():
    create_video()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
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
