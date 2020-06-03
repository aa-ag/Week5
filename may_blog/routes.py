from may_blog import app, db, Message
from flask import render_template, request, redirect, url_for
from may_blog.forms import UserInfoForm, PostForm, LoginForm
from may_blog.models import User, Post, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user


@app.route('/')
def home():
    customer_name = "Aaron"
    order_number = 1
    item_dict = {1: "Ice Cream", 2:"Bread", 3:"Lemons", 4:"Cereal"}
    return render_template("home.html", customer_name = customer_name, order_number = order_number, item_dict = item_dict)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
        
        user = User(username, email, password)
        
        db.session.add(user)
        
        db.session.commit()
        
        msg = Message(f"Thanks for signingup! {email}", recipients=[email])
        msg.body = ('Congrats on sigingup! Looking forward to your posts!')
        msg.html = ('<h1> Welcome to May Blog</h1>' '<p> This will be fun! </p>')

    return render_template('register.html', form = form)

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    post = PostForm()
    if request.method == 'POST' and post.validate():
        title = post.title.data
        content = post.content.data
        print("\n", title, content)
    return render_template('posts.html', post = post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))