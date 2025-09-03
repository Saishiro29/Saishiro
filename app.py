from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

# список статей
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

# детальная страница статьи
@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get_or_404(id)
    return render_template("posts_detail.html", article=article)

@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        db.session.add(article)
        db.session.commit()

        return redirect('/')
    else:
        return render_template("create_update.html", article=None)


# удаление (POST!)
@app.route('/posts/<int:id>/delete', methods=['POST'])
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('posts'))
    except Exception as e:
        return f'Ошибка при удалении: {e}'

# редактирование статьи
@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update_article(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('posts_detail', id=id))
        except Exception as e:
            return f'Ошибка при обновлении: {e}'
    return render_template("create_update.html", article=article)
import secrets; print(secrets.token_hex(16))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
