from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (name TEXT, message TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        if name and message:  # prevent empty messages
            c.execute("INSERT INTO messages VALUES (?, ?)", (name, message))
            conn.commit()

    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    conn.close()

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
