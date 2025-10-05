# CreatorVerse 🚀
A futuristic, AI-powered content creation platform that helps digital creators generate innovative ideas and manage their content calendar with ease.

## 🌟 Features
### 🤖 AI-Powered Content Generation
Generate 5 unique content ideas instantly using OpenAI GPT

Input any topic and get creative suggestions for videos, blogs, and social media

Fallback ideas when API is unavailable

### 📊 Creator Dashboard
Personalized dashboard with your saved ideas

Manual idea addition with categorization

Delete and manage your content ideas

Glassmorphism UI with dark/light mode

### 📅 Content Calendar
Schedule and plan your content releases

Add tasks with specific dates

View all scheduled content in an organized layout

Easy deletion of scheduled tasks

### 🔐 User Management
Secure user registration and authentication

Password reset functionality with secure tokens

Session-based login system

Separate admin portal for platform management

### 👑 Admin Portal
View all users and their activity

Monitor platform analytics

Manage user-generated content

Comprehensive dashboard with statistics

### 🎨 Futuristic UI/UX
Glassmorphism design with neon glow effects

Smooth animations and transitions

Responsive design for all devices

Dark/Light mode toggle

Modern typography (Orbitron & Exo 2 fonts)

## 🛠 Tech Stack
Backend: Flask 2.3.3 (Python)

Database: PostgreSQL with SQLAlchemy ORM

Frontend: HTML5, CSS3, JavaScript

AI Integration: OpenAI GPT-3.5-turbo API

Authentication: Session-based with password hashing

Styling: Glassmorphism CSS with custom animations

## 🚀 Quick Start
Prerequisites
Python 3.8+

PostgreSQL database

OpenAI API key (optional)

### Installation
Clone the repository

``` bash ```
```git clone https://github.com/yourusername/creatorverse.git```
```cd creatorverse```
Create virtual environment 

```bash```
```python -m venv venv```
```source venv/bin/activate  # On Windows: venv\Scripts\activate```
Install dependencies

```bash```
```pip install -r requirements.txt```
Environment Setup
Create a .env file in the root directory:

```env```
```SECRET_KEY=your-super-secret-key-here-make-it-very-long-and-secure```
```DATABASE_URL=postgresql://username:password@localhost/creatorverse```
```OPENAI_API_KEY=your-openai-api-key-here```
Database Setup

```bash```
```# Create PostgreSQL database```
```createdb creatorverse```

```# Or use SQLite (automatically falls back if PostgreSQL not available)```
```# No action needed - will create creatorverse.db automatically```
Run the application

```bash```
```python app.py```
Access the application

Main site: http://localhost:5000

Admin portal: http://localhost:5000/admin

Default Credentials
Admin: admin / admin123

Users: Register through the signup page

## 📁 Project Structure
text
creatorverse/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md             # Project documentation
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet with glassmorphism
│   ├── js/
│   │   └── script.js     # Client-side JavaScript
│   └── images/
│       └── logo.png      # Application logo
└── templates/
    ├── index.html        # Landing page
    ├── signup.html       # User registration
    ├── login.html        # Login page
    ├── forgot_password.html # Password reset request
    ├── reset_password.html  # Password reset form
    ├── dashboard.html    # User dashboard
    ├── calendar.html     # Content calendar
    ├── admin.html        # Admin dashboard
    └── admin_login.html  # Admin login page
## 🔧 API Endpoints
### User Routes
GET / - Landing page

GET/POST /signup - User registration

GET/POST /login - User login

GET/POST /forgot_password - Password reset request

GET/POST /reset_password/<token> - Password reset

GET /logout - User logout

### Dashboard Routes
GET /dashboard - User dashboard

POST /generate_idea - AI idea generation (JSON API)

POST /add_idea - Add manual idea (JSON API)

GET /delete_idea/<id> - Delete idea

### Calendar Routes
GET /calendar - Content calendar

POST /add_schedule - Add schedule (JSON API)

GET /delete_schedule/<id> - Delete schedule

### Admin Routes
GET /admin - Admin dashboard

GET/POST /admin_login - Admin login

### Utility Routes
GET /health - Health check endpoint

## 🎨 UI Components
Glassmorphism Design
Transparent cards with backdrop blur

Neon cyan and purple gradient accents

Smooth hover animations

Futuristic typography

Responsive Layout
Mobile-first design approach

Flexbox and CSS Grid layouts

Adaptive navigation

Interactive Elements
Theme toggle (dark/light mode)

Loading states and animations

Form validation with visual feedback

Confirmation dialogs

## 🔒 Security Features
Password hashing with Werkzeug

Session-based authentication

Secure token generation for password reset

Input validation and sanitization

CSRF protection via Flask sessions

Environment variable configuration
