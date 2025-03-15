import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_change_in_production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'quiz_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-email-password'
    
    # App specific settings
    QUESTIONS_PER_QUIZ = 5
    DEFAULT_QUIZ_TIME = 300  # seconds (5 minutes)
    SOUND_EFFECTS_ENABLED = True
    
    # Media files
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'}
