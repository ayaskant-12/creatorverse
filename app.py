import os
from datetime import datetime, timedelta
import secrets
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///creatorverse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    ideas = db.relationship('Idea', backref='user', lazy=True)
    schedules = db.relationship('Schedule', backref='user', lazy=True)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    task = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match!')
                return render_template('signup.html')
            
            # Check password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long!')
                return render_template('signup.html')
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            
            if existing_user:
                flash('Username already exists!')
                return render_template('signup.html')
            
            if existing_email:
                flash('Email already registered!')
                return render_template('signup.html')
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'true'
        
        if is_admin:
            admin = Admin.query.filter_by(username=username).first()
            if admin and check_password_hash(admin.password, password):
                session['admin_logged_in'] = True
                session['admin_username'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials')
        else:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            # In a real application, you would send an email here
            # For demo purposes, we'll show the reset link
            reset_url = url_for('reset_password', token=reset_token, _external=True)
            flash(f'Password reset link generated. For demo purposes: {reset_url}')
        else:
            flash('No account found with that email address.')
        
        return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user:
        flash('Invalid or expired reset token.')
        return redirect(url_for('forgot_password'))
    
    if user.reset_token_expiry and user.reset_token_expiry < datetime.utcnow():
        flash('Reset token has expired.')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not password or not confirm_password:
            flash('Please fill in all fields.')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('reset_password.html', token=token)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!')
            return render_template('reset_password.html', token=token)
        
        try:
            user.password = generate_password_hash(password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            
            flash('Password reset successfully! Please login with your new password.')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error resetting password: {str(e)}')
            return render_template('reset_password.html', token=token)
    
    return render_template('reset_password.html', token=token)

@app.route('/dashboard')
def dashboard():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    user_ideas = Idea.query.filter_by(user_id=session['user_id']).order_by(Idea.created_at.desc()).all()
    return render_template('dashboard.html', ideas=user_ideas)

@app.route('/calendar')
def calendar():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    user_schedules = Schedule.query.filter_by(user_id=session['user_id']).order_by(Schedule.date).all()
    return render_template('calendar.html', schedules=user_schedules)

@app.route('/generate_idea', methods=['POST'])
def generate_idea():
    if not session.get('user_logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        # Check if OpenAI API key is available
        if not openai.api_key:
            # Return sample ideas for demo if no API key
            sample_ideas = [
                f"1. Create a video series about {topic} for beginners",
                f"2. Write a blog post comparing different approaches to {topic}",
                f"3. Develop an infographic explaining key concepts of {topic}",
                f"4. Host a live Q&A session about {topic} on social media",
                f"5. Create a tutorial series showing practical applications of {topic}"
            ]
            return jsonify({'ideas': sample_ideas})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a creative content strategist. Generate 5 unique, engaging content ideas for digital creators. Return each idea on a new line."
            }, {
                "role": "user",
                "content": f"Generate 5 creative content ideas about: {topic}"
            }],
            max_tokens=500
        )
        
        ideas_text = response.choices[0].message.content
        ideas_list = [idea.strip() for idea in ideas_text.split('\n') if idea.strip()]
        
        # Ensure we have exactly 5 ideas
        while len(ideas_list) < 5:
            ideas_list.append(f"Creative idea about {topic} - explore unique angles")
        
        return jsonify({'ideas': ideas_list[:5]})
    
    except Exception as e:
        # Return sample ideas if OpenAI API fails
        sample_ideas = [
            f"1. Beginner's guide to {topic}",
            f"2. Advanced techniques for {topic}",
            f"3. Common mistakes to avoid in {topic}",
            f"4. Tools and resources for {topic}",
            f"5. Future trends in {topic}"
        ]
        return jsonify({'ideas': sample_ideas})

@app.route('/add_idea', methods=['POST'])
def add_idea():
    if not session.get('user_logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', 'Other').strip()
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        
        new_idea = Idea(
            title=title,
            description=description,
            category=category,
            user_id=session['user_id']
        )
        db.session.add(new_idea)
        db.session.commit()
        
        return jsonify({
            'message': 'Idea added successfully', 
            'id': new_idea.id
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error adding idea: {str(e)}")
        return jsonify({'error': f'Failed to add idea: {str(e)}'}), 500

@app.route('/delete_idea/<int:idea_id>')
def delete_idea(idea_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    try:
        idea = Idea.query.get_or_404(idea_id)
        if idea.user_id != session['user_id']:
            flash('Unauthorized action')
            return redirect(url_for('dashboard'))
        
        db.session.delete(idea)
        db.session.commit()
        flash('Idea deleted successfully')
    
    except Exception as e:
        flash(f'Error deleting idea: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    if not session.get('user_logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        date = data.get('date', '').strip()
        task = data.get('task', '').strip()
        
        if not date:
            return jsonify({'error': 'Date is required'}), 400
        if not task:
            return jsonify({'error': 'Task description is required'}), 400
        
        new_schedule = Schedule(
            date=date,
            task=task,
            user_id=session['user_id']
        )
        db.session.add(new_schedule)
        db.session.commit()
        
        return jsonify({
            'message': 'Schedule added successfully', 
            'id': new_schedule.id
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error adding schedule: {str(e)}")
        return jsonify({'error': f'Failed to add schedule: {str(e)}'}), 500

@app.route('/delete_schedule/<int:schedule_id>')
def delete_schedule(schedule_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    try:
        schedule = Schedule.query.get_or_404(schedule_id)
        if schedule.user_id != session['user_id']:
            flash('Unauthorized action')
            return redirect(url_for('calendar'))
        
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted successfully')
    
    except Exception as e:
        flash(f'Error deleting schedule: {str(e)}')
    
    return redirect(url_for('calendar'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    users = User.query.all()
    ideas = Idea.query.all()
    schedules = Schedule.query.all()
    
    stats = {
        'total_users': len(users),
        'total_ideas': len(ideas),
        'total_schedules': len(schedules)
    }
    
    return render_template('admin.html', users=users, ideas=ideas, schedules=schedules, stats=stats)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials')
    
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint to verify the app is running"""
    try:
        # Test database connection
        user_count = User.query.count()
        admin_count = Admin.query.count()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'users_count': user_count,
            'admins_count': admin_count,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

def initialize_database():
    """Initialize the database with required tables and default admin only"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create default admin user if it doesn't exist
            if not Admin.query.first():
                admin = Admin(
                    username='admin',
                    password=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Default admin user created (admin/admin123)")
            
            print("🎉 Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Database initialization error: {str(e)}")
            # Try to create basic tables even if sample data fails
            try:
                db.create_all()
                print("✅ Basic tables created")
            except Exception as e2:
                print(f"❌ Critical error: {e2}")

# Initialize database when app starts
initialize_database()

if __name__ == '__main__':
    print("\n🌟 CreatorVerse Starting Up...")
    print("📍 Available Routes:")
    print("   - Home: http://localhost:5000")
    print("   - Signup: http://localhost:5000/signup")
    print("   - Login: http://localhost:5000/login")
    print("   - Admin: http://localhost:5000/admin")
    print("   - Health Check: http://localhost:5000/health")
    print("\n🔑 Default Admin Credentials:")
    print("   - Admin: admin / admin123")
    print("\n🚀 Starting Flask development server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
