from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return (
            f"<Author id={self.id}, "
            f"name='{self.name}', "
            f"birth_date={self.birth_date}, "
            f"date_of_death={self.date_of_death}>"
        )

    def __str__(self):
        return f"{self.name} ({self.birth_date}–{self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship('Author', backref='books')


    def __repr__(self):
        return (
            f"<Book id={self.id}, title='{self.title}', "
            f"isbn='{self.isbn}', publication_year={self.publication_year}, "
            f"author_id={self.author_id}>"
        )

    def __str__(self):
        return f"'{self.title}' ({self.publication_year})"
