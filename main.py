import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params = json.load(c)["param"]


app = Flask(__name__)
app.secret_key = 'super-secret-key'
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = params['gmail_user']
app.config['MAIL_PASSWORD'] = "kqkrxofpgmmefbei"
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

# setting up local mySQL database by making a connection to it 
if params['locol_server'] == True:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['locol_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db=SQLAlchemy(app)


# connecting to "__CONTACTS__" database in my mySQL database 
class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    def __init__(self, name, email, phone_num, message, date):
        self.name = name
        self.email = email
        self.phone_num = phone_num
        self.message = message
        self.date = date


# connecting to "__POST__" database in my mySQL database 
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    subheading = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)




@app.route("/")
def start():
    post = Posts.query.filter_by().all()[0:params['no_of_posts']]
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('index.html', co=params, posts = post, username=session['user'])
    else:
        return render_template('index.html', co=params, posts = post)



@app.route("/home")
def home():
    return render_template('index.html',co=params)


@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():

    post = Posts.query.all()

    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard.html', co=params, post=post, username=session['user'])

    if request.method=='POST':
        username = request.form.get('user_name')
        userpass = request.form.get('pass')
        if ( username == params['admin_user'] and userpass == params['admin_password'] ):
            session['user'] = username
            return render_template('dashboard.html', co=params, post=post, username=session['user'])

    return render_template('login.html',co=params)


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            # Process the form submission and update the post
            box_title = request.form.get('title')
            subheading = request.form.get('subheading')
            slug = request.form.get('slug')
            content = request.form.get('content')
            date = datetime.now()
            if sno == '0':
                post = Posts(title=box_title, subheading=subheading, slug=slug, content=content, date=date)
                db.session.add(post)
                db.session.commit()
                return redirect('/dashboard')
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.subheading = subheading
                post.slug = slug
                post.content = content
                post.date = date
                db.session.commit()
                return redirect('/edit/' + sno)
        else:
            # Fetch the post from the database and render the edit form
            post = Posts.query.filter_by(sno=sno).first()
            return render_template('edit.html', co=params, post=post, sno=sno)
    return render_template('index.html')
     

# @app.route("/post")
# def SamplePost():
#     return render_template('post.html', co=params)


@app.route("/post")
def SamplePost():
    return render_template('post.html', co=params)



@app.route("/post/<string:post_slug>", methods = ['GET'] )
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', co=params, post=post)


@app.route("/about")
def about():
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('about.html',co=params, username=session['user'])
    else:
        return render_template('about.html',co=params)


@app.route("/contact", methods = ['GET','POST'])
def contact():
    if (request.method=='POST'):
        '''ADD RQUEST TO THE DATABASE'''
        new_name = request.form.get('name')
        new_email =request.form.get('email')
        new_phone_num = request.form.get('phone')
        new_message = request.form.get('message')
        entry = contacts(name=new_name, email=new_email, phone_num=new_phone_num, message=new_message, date=datetime.now())
        db.session.add(entry)  # Add the entry to the session
        db.session.commit()    # Commit the changes to the database
        mail.send_message(f'New message from {new_name}',
                          sender = new_email,
                          recipients = [params['gmail_user']],
                          body = f'{new_message}\n{new_phone_num}')

    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('contact.html', co=params, username=session['user'])
    else:
        return render_template('contact.html', co=params)

@app.route("/uploder", methods= ['GET', 'POST'])
def uploder():
    if ('user' in session and session['user'] == params['admin_user']):    
        if request.method == 'POST':
            f = request.files['temp_filename_from_html']
            f.save(os.path.join(params['uplode_location'], secure_filename(f.filename)  ))
            return 'Uploded Successfully'
    return 'Access Denied'
        
        
@app.route("/delete/<string:sno>", methods= ['GET', 'POST'])
def delete(sno):
        post_to_delete = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/dashboard')


@app.route("/logout")
def logout():
    session.pop('user', None)  # Remove 'user' from the session to log the user out
    return render_template('/logout.html', co=params)








if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)




