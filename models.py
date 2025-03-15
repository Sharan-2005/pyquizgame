from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # For production, use password hashing
    email = db.Column(db.String(120), unique=True, nullable=True)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User preferences
    show_timer = db.Column(db.Boolean, default=True)
    sound_effects = db.Column(db.Boolean, default=True)
    dark_theme = db.Column(db.Boolean, default=False)
    default_difficulty = db.Column(db.String(20), default='medium')
    
    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True, cascade="all, delete-orphan")
    question_history = db.relationship('UserQuestion', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    # Store options as a JSON string
    options = db.Column(db.String(512), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    category = db.Column(db.String(50), default='python')  # python, general, etc.

    def get_options(self):
        return json.loads(self.options)
        
    def __repr__(self):
        return f"Quiz('{self.question[:30]}...', '{self.difficulty}', '{self.category}')"

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    difficulty = db.Column(db.String(20), default='medium')
    time_taken = db.Column(db.Integer, nullable=True)  # Time taken in seconds
    
    def __repr__(self):
        return f"QuizResult('{self.user_id}', Score: {self.score}/{self.total_questions}, {self.percentage}%)"

class UserQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    date_shown = db.Column(db.DateTime, default=datetime.utcnow)
    quiz_session = db.Column(db.String(64), nullable=True)  # To group questions shown in the same quiz
    was_correct = db.Column(db.Boolean, nullable=True)  # If the user answered correctly
    
    # Establish a unique constraint to ensure a user-question pair is unique
    __table_args__ = (db.UniqueConstraint('user_id', 'question_id', 'quiz_session', name='_user_question_session_uc'),)
    
    def __repr__(self):
        return f"UserQuestion(User: {self.user_id}, Question: {self.question_id}, Session: {self.quiz_session})"
