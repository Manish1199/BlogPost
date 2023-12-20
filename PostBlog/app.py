from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime  # Import datetime module

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    posts = Post.query.all()
    print(posts)
    return render_template('index.html', posts=posts)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            pub_date_str = request.form['pub_date']

            # Convert pub_date to datetime object
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')

            new_post = Post(title=title, content=content, pub_date=pub_date)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('homepage'))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding post: {str(e)}")

    posts = Post.query.all()
    return render_template('admin.html', posts=posts)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/other_page')
def other_page():
    return render_template('other_page.html')

if __name__ == '__main__':
    app.run(debug=True)
