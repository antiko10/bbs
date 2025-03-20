from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
import os
from database import init_db, add_book, get_all_books, add_category, get_all_categories, delete_book, delete_category, edit_book, edit_category

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Admin credentials
ADMIN_USERNAME = 'antiko'
ADMIN_PASSWORD = 'antiko2123'

# Ensure upload folders exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'covers'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs'), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you would typically send this to admin via email or store in DB
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    books = get_all_books()
    categories = get_all_categories()
    return render_template('admin_dashboard.html', 
                         books=books,
                         categories=categories,
                         total_books=len(books), 
                         total_categories=len(categories))

@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book_route():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        order = request.form['order']
        cover = request.files['cover']
        pdf = request.files['pdf']
        
        cover_filename = secure_filename(cover.filename)
        pdf_filename = secure_filename(pdf.filename)
        
        cover_path = os.path.join(app.config['UPLOAD_FOLDER'], 'covers', cover_filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs', pdf_filename)
        
        cover.save(cover_path)
        pdf.save(pdf_path)
        
        add_book(title, category, order, cover_filename, pdf_filename)
        flash('Book added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_book.html', categories=get_all_categories())

@app.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book_route(book_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        order = request.form['order']
        edit_book(book_id, title, category, order)
        flash('Book updated successfully!')
        return redirect(url_for('admin_dashboard'))
    book = next((b for b in get_all_books() if b['id'] == book_id), None)
    return render_template('add_book.html', book=book, categories=get_all_categories())

@app.route('/admin/delete_book/<int:book_id>')
def delete_book_route(book_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    delete_book(book_id)
    flash('Book deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_category', methods=['GET', 'POST'])
def add_category_route():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        add_category(name)
        flash('Category added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_category.html')

@app.route('/admin/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category_route(category_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        edit_category(category_id, name)
        flash('Category updated successfully!')
        return redirect(url_for('admin_dashboard'))
    category = next((c for c in get_all_categories() if c['id'] == category_id), None)
    return render_template('add_category.html', category=category)

@app.route('/admin/delete_category/<int:category_id>')
def delete_category_route(category_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    delete_category(category_id)
    flash('Category deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/bookstore')
def bookstore():
    search_query = request.args.get('search', '').lower()
    all_books = get_all_books()
    
    if search_query:
        # Filter books based on title or category
        books = [book for book in all_books 
                if search_query in book['title'].lower() 
                or search_query in book['category'].lower()]
    else:
        books = all_books
        
    return render_template('bookstore.html', books=books)

@app.route('/download/<pdf_filename>')
def download_book(pdf_filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs', pdf_filename), as_attachment=True)

if __name__ == '__main__':
    init_db()
    # Get the PORT environment variable if it exists (usually for cloud platforms)
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
