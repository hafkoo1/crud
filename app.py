
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()

    return render_template('index.html', books=books)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (title, author) VALUES (?, ?)',
            (title, author)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn.execute(
            'UPDATE books SET title = ?, author = ? WHERE id = ?',
            (title, author, id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    book = conn.execute(
        'SELECT * FROM books WHERE id = ?', (id,)
    ).fetchone()

    conn.close()

    return render_template('edit.html', book=book)


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()

    conn.execute('DELETE FROM books WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')

    conn.close()

    app.run(debug=True)
