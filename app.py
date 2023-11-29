from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'fdad3e6859d4e5edfbb7e5e99a68c3c6'  # secret key

# Function to connect to the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('user.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Create the 'users' table if it doesn't exist
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        messages = get_flashed_messages()
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username already exists', 'error')
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            session['username'] = username
            flash('Registration successful', 'success')
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return f'Welcome, {username}! This is your dashboard.'
    else:
        return redirect(url_for('register'))

# routes for HTML pages
@app.route('/laptops.html')
def laptops():
    return render_template('laptops.html')

@app.route('/books.html')
def books():
    return render_template('books.html')

@app.route('/accessories.html')
def accessories():
    return render_template('accessories.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the 'username' from the session
    return render_template('logout.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize the database
    app.run(debug=True)
