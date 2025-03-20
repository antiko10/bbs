import sqlite3

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  category TEXT NOT NULL,
                  order_num INTEGER,
                  cover_path TEXT,
                  pdf_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_book(title, category, order, cover_path, pdf_path):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO books (title, category, order_num, cover_path, pdf_path) VALUES (?, ?, ?, ?, ?)',
              (title, category, order, cover_path, pdf_path))
    conn.commit()
    conn.close()

def add_category(name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_db_connection()
    c = conn.cursor()
    books = c.execute('SELECT * FROM books ORDER BY order_num').fetchall()
    conn.close()
    return books

def get_all_categories():
    conn = get_db_connection()
    c = conn.cursor()
    categories = c.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return categories

def delete_book(book_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

def edit_book(book_id, title, category, order):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE books SET title = ?, category = ?, order_num = ? WHERE id = ?',
              (title, category, order, book_id))
    conn.commit()
    conn.close()

def edit_category(category_id, name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
    conn.commit()
    conn.close()