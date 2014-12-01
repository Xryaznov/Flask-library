
from flask import render_template, request, flash, session, redirect, url_for, Flask
from forms import SignupForm, SigninForm, AddbookForm
from models import db, User, Book, Author

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getjson')
def getjson():
    books = dict()
    bookset = db.session.execute("select distinct book_id from library")

    for row in bookset:
        books[Book.query.get(row['book_id'])] = []

    for book in books:
        authorset = db.session.execute(
            "select id from authors inner join library on authors.id = library.author_id where book_id = " + str(
                book.id) + ";")
        for row in authorset:
            books[book].append(Author.query.get(row['id']).name.encode("utf-8"))

    data = []

    for book in books:
        dataitem = {'id': 1, 'title': 'title', 'authors': 'authors'}
        dataitem['id'] = book.id
        dataitem['title'] = book.title
        dataitem['authors'] = books[book]

        data.append(dataitem)

    import json

    return json.dumps(data)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email=session['email']).first()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)





@app.route('/admintest')
def admintest():
    return redirect('/admin')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('home'))






@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    form = AddbookForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('addbook.html', form=form)
        else:
            book = Book(form.title.data)
            author = Author(form.author.data)

            existing_book = Book.query.filter_by(title=form.title.data).first()
            existing_author = Author.query.filter_by(name=form.author.data).first()

            if existing_book is not None:
                book = existing_book
            else:
                db.session.add(book)

            if existing_author is not None:
                author = existing_author
            else:
                db.session.add(author)

            db.session.commit()

            db.session.execute(
                "insert into library (book_id, author_id) values ({0}, {1})".format(str(book.id), str(author.id)))
            db.session.commit()

            return redirect(url_for('addbook'))

    elif request.method == 'GET':
        return render_template('addbook.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
