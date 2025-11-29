from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        author_name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')
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
    books = Book.query.all()
    return render_template('home.html', books=books)


"""
# Only run once to create the tables
with app.app_context():
    db.create_all()
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)