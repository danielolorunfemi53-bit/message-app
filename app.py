from flask import Flask, render_template, request
import sqlite3
import os  # Needed for Render

app = Flask(__name__)

# Database initialization
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
        if name and message:
            c.execute("INSERT INTO messages VALUES (?, ?)", (name, message))
            conn.commit()

    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    conn.close()

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    # Make it compatible with Render hosting
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
