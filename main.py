from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


# import sqlalchemy
###### SQLITE3 MODULE ######
# import sqlite3
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()
##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'



@app.route('/')
def home():
    all_books = Book.query.all()
    print(all_books)
    return render_template("index.html", data=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        rating = request.form['rating']
        new_book = Book(title=name, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()

        return redirect(url_for('home'))
    book_id = request.args.get('id')
    return render_template("edit.html", book=Book.query.get(book_id))

@app.route("/delete", methods=["GET", "POST"])
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    # with app.app_context():
    #     # Create database
    #     # db.create_all()
    #     entry = Book(title="The Seven dkingddom", author="Taylor Jenkins Reid", rating="9.5")
    #     db.session.add(entry)
    #     db.session.commit()

    app.run(debug=True)

#
# Create A New Record
# new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
# db.session.add(new_book)
# db.session.commit()
# NOTE: When creating new records, the primary key fields is optional. you can also write:
#
# new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
#
# the id field will be auto-generated.
#
#
#
# Read All Records
# all_books = db.session.query(Book).all()
# or
# all_books = Book.query.all()

# Read A Particular Record By Query
# book = Book.query.filter_by(title="Harry Potter").first()
#
#
# Update A Particular Record By Query
# book_to_update = Book.query.filter_by(title="Harry Potter").first()
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()
#
#
# Update A Record By PRIMARY KEY
# book_id = 1
# book_to_update = Book.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"
# db.session.commit()
#
#
# Delete A Particular Record By PRIMARY KEY
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()
# You can also delete by querying for a particular value e.g. by title or one of the other properties.
