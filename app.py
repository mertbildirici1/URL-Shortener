from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                          (id INTEGER PRIMARY KEY, short TEXT, full TEXT)''')
        db.commit()

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_url = request.form['full_url']
        short_url = generate_short_url()

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO urls (short, full) VALUES (?, ?)', (short_url, full_url))
        db.commit()

        flash(f'Short URL is: {request.host_url}{short_url}')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT full FROM urls WHERE short = ?', (short_url,))
    result = cursor.fetchone()

    if result:
        return redirect(result[0])
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
