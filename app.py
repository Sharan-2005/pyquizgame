
import os
import json
import time
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from models import db, User, Quiz, QuizResult, UserQuestion
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()
    if Quiz.query.count() == 0:
        # Predefined Python multiple-choice questions
        python_questions = [
            {
                "question": "What is the output of print(2 ** 3)?",
                "answer": "8",
                "options": ["6", "8", "9", "7"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "Which of the following is a mutable data type in Python?",
                "answer": "List",
                "options": ["Tuple", "List", "String", "Integer"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What does the 'len()' function do?",
                "answer": "Returns the length of an object",
                "options": ["Returns the type of an object", "Calculates the value", "Returns the length of an object", "None of the above"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "Which keyword is used for function declaration in Python?",
                "answer": "def",
                "options": ["function", "def", "func", "declare"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What does the 'in' keyword do in Python?",
                "answer": "Checks for membership",
                "options": ["Checks for equality", "Checks for membership", "Assigns a value", "None of the above"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "Which of the following is used to handle exceptions in Python?",
                "answer": "try-except",
                "options": ["if-else", "try-except", "for-in", "switch-case"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What is the time complexity of dictionary lookups in Python?",
                "answer": "O(1) on average",
                "options": ["O(n)", "O(log n)", "O(1) on average", "O(n²)"],
                "difficulty": "hard",
                "category": "python"
            },
            {
                "question": "What is a decorator in Python?",
                "answer": "A function that modifies another function",
                "options": ["A class method", "A type of loop", "A function that modifies another function", "A variable declaration"],
                "difficulty": "hard",
                "category": "python"
            },
            # Additional Python questions
            {
                "question": "What is the output of print(list(range(5)))?",
                "answer": "[0, 1, 2, 3, 4]",
                "options": ["[0, 1, 2, 3, 4]", "[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4, 5]", "[1, 2, 3, 4]"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "Which method is used to add an element to a list in Python?",
                "answer": "append()",
                "options": ["add()", "push()", "append()", "insert()"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What is the result of 10 / 3 in Python 3?",
                "answer": "3.3333333333333335",
                "options": ["3", "3.3", "3.33", "3.3333333333333335"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "How do you create a dictionary in Python?",
                "answer": "{'key': 'value'}",
                "options": ["['key': 'value']", "{'key': 'value'}", "('key': 'value')", "<'key': 'value'>"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What is a lambda function in Python?",
                "answer": "An anonymous function defined using the lambda keyword",
                "options": ["A built-in function", "A math function", "An anonymous function defined using the lambda keyword", "A type of loop"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What does the 'zip()' function do in Python?",
                "answer": "Returns an iterator of tuples where the i-th tuple contains the i-th element from each of the argument sequences",
                "options": ["Compresses files", "Returns an iterator of tuples where the i-th tuple contains the i-th element from each of the argument sequences", "Combines two lists", "Creates a dictionary from two lists"],
                "difficulty": "hard",
                "category": "python"
            },
            {
                "question": "What is a generator in Python?",
                "answer": "A function that returns an iterator using the yield keyword",
                "options": ["A class method", "A function that returns an iterator using the yield keyword", "A tool to generate random numbers", "A built-in function"],
                "difficulty": "hard",
                "category": "python"
            },
            {
                "question": "How is memory managed in Python?",
                "answer": "Through automatic garbage collection",
                "options": ["Through manual allocation and deallocation", "Through automatic garbage collection", "Through reference counting only", "Python does not manage memory"],
                "difficulty": "hard",
                "category": "python"
            },
            {
                "question": "What is the result of '3' + '4' in Python?",
                "answer": "'34'",
                "options": ["7", "'34'", "34", "Error"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What are *args and **kwargs in Python function definitions?",
                "answer": "Ways to pass a variable number of arguments to a function",
                "options": ["Error handlers", "Ways to declare private variables", "Ways to pass a variable number of arguments to a function", "Import statements"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What does the 'global' keyword do in Python?",
                "answer": "Declares a global variable inside a function",
                "options": ["Creates a new module", "Imports all modules", "Declares a global variable inside a function", "Defines a constant"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What is PEP 8 in Python?",
                "answer": "Style guide for Python code",
                "options": ["A built-in module", "Style guide for Python code", "A type of loop", "A debugging tool"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "Which method is used to remove and return an element from a list in Python?",
                "answer": "pop()",
                "options": ["remove()", "delete()", "pop()", "discard()"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What is the purpose of __init__ method in Python classes?",
                "answer": "Constructor that is called when an object is created",
                "options": ["Destructor", "Constructor that is called when an object is created", "Iterator", "Finalizer"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What is the output of print(bool(0), bool(1))?",
                "answer": "False True",
                "options": ["True True", "False False", "False True", "True False"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What does the 'self' keyword represent in a Python class?",
                "answer": "Reference to the current instance of the class",
                "options": ["Reference to the current module", "Reference to the parent class", "Reference to the current instance of the class", "Reference to the current function"],
                "difficulty": "medium",
                "category": "python"
            },
            {
                "question": "What is the purpose of the 'pass' statement in Python?",
                "answer": "A null statement that does nothing",
                "options": ["To skip a loop iteration", "To exit a function", "A null statement that does nothing", "To raise an exception"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What is the output of print([1, 2, 3] * 2)?",
                "answer": "[1, 2, 3, 1, 2, 3]",
                "options": ["[1, 2, 3, 1, 2, 3]", "[2, 4, 6]", "[1, 4, 9]", "Error"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What is the correct way to create a set in Python?",
                "answer": "{1, 2, 3}",
                "options": ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "<1, 2, 3>"],
                "difficulty": "easy",
                "category": "python"
            },
            {
                "question": "What is the purpose of the 'with' statement in Python?",
                "answer": "Ensures proper acquisition and release of resources",
                "options": ["Loop control", "Error handling", "Ensures proper acquisition and release of resources", "Import management"],
                "difficulty": "medium",
                "category": "python"
            }
        ]
        # Add questions to the database
        for question in python_questions:
            quiz_question = Quiz(**question)
            db.session.add(quiz_question)
        db.session.commit()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # For simplicity in this example, but in production should use password hashing
        if user and user.password == password:
            login_user(user)
            session['theme'] = 'dark' if user.dark_theme else 'light'
            session['sound_effects'] = user.sound_effects
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            # For simplicity in this example; in production, use password hashing
            new_user = User(
                username=username, 
                password=password,
                email=email,
                date_registered=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get all user's quiz results
    user_results = QuizResult.query.filter_by(user_id=current_user.id)\
                           .order_by(QuizResult.date_taken.desc())\
                           .all()
    
    # Prepare data for charts
    labels = []
    scores = []
    
    for result in user_results:
        # Format date as DD/MM HH:MM
        labels.append(result.date_taken.strftime('%d/%m %H:%M'))
        scores.append(result.percentage)
    
    # If no results yet, provide placeholder data
    if not labels:
        labels = ["No Data"]
        scores = [0]
    
    # Get overall stats
    total_quizzes = len(user_results)
    avg_score = 0
    highest_score = 0
    
    if total_quizzes > 0:
        avg_score = sum(scores) / total_quizzes
        avg_score = round(avg_score, 1)
        highest_score = max(scores)
    
    # Get top 10 users for leaderboard
    # This query gets the highest score for each user
    leaderboard_query = db.session.query(
        User.username,
        db.func.max(QuizResult.percentage).label('max_score'),
        db.func.count(QuizResult.id).label('quiz_count')
    ).join(QuizResult, User.id == QuizResult.user_id)\
     .group_by(User.id)\
     .order_by(db.desc('max_score'))\
     .limit(10).all()
    
    leaderboard = []
    for username, max_score, quiz_count in leaderboard_query:
        leaderboard.append({
            'username': username,
            'max_score': round(max_score, 1),
            'quiz_count': quiz_count
        })
    
    # Get all quiz attempts with details
    quiz_history = []
    for i, result in enumerate(user_results):
        quiz_history.append({
            'attempt': i+1,
            'date': result.date_taken.strftime('%d/%m/%Y %H:%M'),
            'score': result.percentage,
            'correct': result.score,
            'total': result.total_questions
        })
    
    return render_template(
        'dashboard.html',
        labels=labels,
        scores=scores,
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        highest_score=highest_score,
        user_results=user_results,
        leaderboard=leaderboard,
        quiz_history=quiz_history
    )

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    # Handle form submission
    if request.method == 'POST':
        question_ids = request.form.getlist('question_id')
        quiz_session = request.form.get('quiz_session', datetime.utcnow().strftime('%Y%m%d%H%M%S'))
        
        # Calculate score
        score = 0
        total_questions = len(question_ids)
        
        # Process each question's answer
        for q_id in question_ids:
            answer_key = f"answer_{q_id}"
            if answer_key in request.form:
                user_answer = request.form[answer_key]
                question = Quiz.query.get(int(q_id))
                
                # Compare the user's answer with the correct answer
                correct = question and user_answer.lower().strip() == question.answer.lower().strip()
                if correct:
                    score += 1
                
                # Record this question as shown to the user
                user_question = UserQuestion(
                    user_id=current_user.id,
                    question_id=int(q_id),
                    quiz_session=quiz_session,
                    was_correct=correct
                )
                db.session.add(user_question)
        
        # Calculate time taken if available
        time_taken = None
        if 'quiz_start_time' in session:
            start_time = datetime.fromisoformat(session['quiz_start_time'])
            time_taken = (datetime.utcnow() - start_time).total_seconds()
            session.pop('quiz_start_time', None)
        
        # Format time taken for display
        formatted_time = None
        if time_taken:
            minutes = int(time_taken // 60)
            seconds = int(time_taken % 60)
            formatted_time = f"{minutes:02d}:{seconds:02d}"
        
        # Calculate percentage
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # Determine sound effect based on score
        sound_effect = 'tryagain'
        if percentage >= 90:
            sound_effect = 'victory'
        elif percentage >= 70:
            sound_effect = 'success'
        elif percentage >= 50:
            sound_effect = 'complete'
        
        # Save result to database
        quiz_result = QuizResult(
            user_id=current_user.id,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            time_taken=time_taken,
            difficulty=session.get('quiz_difficulty', 'medium')
        )
        db.session.add(quiz_result)
        db.session.commit()
        
        # Store data needed for the score page
        session['score'] = score
        session['total_questions'] = total_questions
        session['percentage'] = percentage
        session['time_taken'] = formatted_time
        session['sound_effect'] = sound_effect
        
        # Redirect to score page
        return redirect(url_for('score'))
    
    # GET request: Display quiz
    difficulty = request.args.get('difficulty', current_user.default_difficulty or 'medium')
    num_questions = min(int(request.args.get('num_questions', app.config.get('QUESTIONS_PER_QUIZ', 5))), 10)
    
    # Create a unique session ID for this quiz attempt
    quiz_session = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    
    # Store the start time in the session
    session['quiz_start_time'] = datetime.utcnow().isoformat()
    session['quiz_difficulty'] = difficulty
    
    # Get all questions of the selected difficulty
    all_questions = Quiz.query.filter_by(difficulty=difficulty).all()
    
    # Get IDs of questions this user has already seen in the last 24 hours
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    recent_question_ids = db.session.query(UserQuestion.question_id)\
                         .filter(UserQuestion.user_id == current_user.id)\
                         .filter(UserQuestion.date_shown >= one_day_ago)\
                         .distinct().all()
    recent_question_ids = [q[0] for q in recent_question_ids]
    
    # Filter out questions the user has recently seen
    unseen_questions = [q for q in all_questions if q.id not in recent_question_ids]
    
    # If not enough unseen questions, fill with random questions from the full set
    if len(unseen_questions) < num_questions:
        # Calculate how many more questions we need
        more_needed = num_questions - len(unseen_questions)
        
        # Get IDs of all questions we already selected
        selected_ids = [q.id for q in unseen_questions]
        
        # From all questions, filter out those we've already selected
        remaining_questions = [q for q in all_questions if q.id not in selected_ids]
        
        # Randomly select additional questions
        if remaining_questions:
            additional_questions = random.sample(remaining_questions, min(more_needed, len(remaining_questions)))
            unseen_questions.extend(additional_questions)
    
    # If we have more unseen questions than needed, randomly select the required number
    if len(unseen_questions) > num_questions:
        questions = random.sample(unseen_questions, num_questions)
    else:
        questions = unseen_questions
    
    return render_template(
        'quiz.html', 
        questions=questions, 
        quiz_session=quiz_session,
        enumerate=enumerate,
        difficulty=difficulty.capitalize(),
        sound_enabled=session.get('sound_effects', True),
        theme=session.get('theme', 'light')
    )

@app.route('/score')
@login_required
def score():
    # Get quiz results from session
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    percentage = session.get('percentage', 0)
    time_taken = session.get('time_taken', None)
    sound_effect = session.get('sound_effect', 'complete')
    
    # Create appropriate message based on score
    message = 'Practice makes perfect!'
    if percentage >= 90:
        message = 'Outstanding! You\'re a quiz master! 🏆'
    elif percentage >= 70:
        message = 'Great job! You really know your stuff! 🌟'
    elif percentage >= 50:
        message = 'Good effort! Keep practicing! 👍'
    
    # Clean up session
    for key in ['score', 'total_questions', 'percentage', 'time_taken', 'sound_effect']:
        if key in session:
            session.pop(key)
    
    return render_template(
        'score.html',
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        time_taken=time_taken,
        sound=f"{sound_effect}.mp3",
        message=message,
        num_questions=total_questions,
        sound_enabled=session.get('sound_effects', True),
        theme=session.get('theme', 'light')
    )

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Check which form was submitted based on the button name
        if 'update_profile' in request.form:
            # Handle profile update
            username = request.form.get('username')
            email = request.form.get('email')
            
            # Update username if provided and not already taken
            if username and username != current_user.username:
                if User.query.filter_by(username=username).first() and User.query.filter_by(username=username).first().id != current_user.id:
                    flash('Username already taken', 'error')
                    return redirect(url_for('settings'))
                current_user.username = username
            
            # Update email if provided
            if email:
                current_user.email = email
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        elif 'update_password' in request.form:
            # Handle password update
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate current password (using plain text comparison since that's how login works)
            if current_user.password != current_password:
                flash('Current password is incorrect', 'error')
                return redirect(url_for('settings'))
            
            # Validate new password
            if len(new_password) < 8:
                flash('Password must be at least 8 characters long', 'error')
                return redirect(url_for('settings'))
                
            # Confirm passwords match
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('settings'))
            
            # Update password (plain text, matching the existing authentication system)
            current_user.password = new_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            
        elif 'update_preferences' in request.form:
            # Update user preferences from form
            current_user.show_timer = 'show_timer' in request.form
            current_user.sound_effects = 'sound_effects' in request.form
            
            # Update default difficulty if provided
            difficulty = request.form.get('difficulty')
            if difficulty in ['easy', 'medium', 'hard']:
                current_user.default_difficulty = difficulty
            
            # Save changes
            db.session.commit()
            
            # Update session variables for sound effects
            session['sound_effects'] = current_user.sound_effects
            
            flash('Preferences updated successfully!', 'success')
        
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    
    # If user is logged in, save preference
    if current_user.is_authenticated:
        current_user.dark_theme = (new_theme == 'dark')
        db.session.commit()
    
    return jsonify({'success': True, 'theme': new_theme})

@app.route('/toggle-sound', methods=['POST'])
def toggle_sound():
    sound_enabled = session.get('sound_effects', True)
    session['sound_effects'] = not sound_enabled
    
    # If user is logged in, save preference
    if current_user.is_authenticated:
        current_user.sound_effects = not sound_enabled
        db.session.commit()
    
    return jsonify({'success': True, 'sound_enabled': not sound_enabled})

@app.context_processor
def inject_theme():
    # Make theme and sound_effects available in all templates
    return {
        'theme': session.get('theme', 'light'),
        'sound_enabled': session.get('sound_effects', True)
    }

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
