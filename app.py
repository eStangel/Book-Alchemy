from pyexpat.errors import messages

from flask import Flask, render_template, request, redirect, url_for
import os
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    """Handles adding a new author via a form."""
    if request.method == 'POST':
        author_name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        date_of_death = (
            datetime.strptime(date_of_death_str, "%Y-%m-%d").date()
            if date_of_death_str else None
        )

        if author_name and birth_date and date_of_death:
            new_author = Author(
                name = author_name,
                birth_date = birth_date,
                date_of_death = date_of_death
            )
            db.session.add(new_author)
            db.session.commit()

            success_message = f"Author '{author_name}' added successfully!"
        else:
            success_message = "Error: Fill out all fields!"

        return render_template('add_author.html', success_message=success_message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handles adding a new book via a form."""
    # Fetch all authors from database
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        if title and isbn and publication_year and author_id:
            new_book = Book(
                title = title,
                isbn = isbn,
                publication_year = publication_year,
                author_id = author_id
            )
            db.session.add(new_book)
            db.session.commit()

            success_message = f"Book '{title}' added successfully!"
        else:
            success_message = "Error: Fill out all fields!"

        return render_template('add_book.html', authors=authors, success_message=success_message)

    return render_template('add_book.html', authors=authors)


@app.route('/home')
def home():
    """Displays all books, with optional sorting and search functionality."""
    books = Book.query.all()
    message = request.args.get('message')

    sort_option = request.args.get('sort')
    search_query = request.args.get('query')

    if sort_option == 'author_asc':
        books = sorted(books, key=lambda b: b.author.name.split()[-1])
    elif sort_option == 'author_desc':
        books = sorted(books, key=lambda b: b.author.name.split()[-1], reverse=True)
    elif sort_option == 'book_name_asc':
        books = db.session.query(Book).order_by(Book.title.asc()).all()
    elif sort_option == 'book_name_desc':
        books = db.session.query(Book).order_by(Book.title.desc()).all()
    if search_query:
        books = db.session.query(Book) \
            .filter(Book.title.ilike(f"%{search_query}%")) \
            .all()

    return render_template('home.html', books=books, message=message)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete(book_id):
    """Deletes a book and its author if no other books exist for them."""
    book = db.session.get(Book, book_id)
    if not book:
        return redirect(url_for('home', message="Error: Book not found!"))

    author = book.author
    db.session.delete(book)
    db.session.commit()

    if len(author.books) == 0:
        db.session.delete(author)
        db.session.commit()

    return redirect(url_for('home', message="Book successfully deleted!"))


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """Deletes an author and all associated books."""
    author = db.session.get(Author, author_id)
    if not author:
        return redirect(url_for('home', message="Error: Author not found!"))

    for book in list(author.books):
        db.session.delete(book)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('home', message="Author and all associated books deleted!"))


@app.route('/book/<int:book_id>/details')
def details(book_id):
    """Displays detailed information for a specific book."""
    book = db.session.get(Book, book_id)
    return render_template('book_details.html', book=book)


"""
# Only run once to create the tables
with app.app_context():
    db.create_all()
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)