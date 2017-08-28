# ---- Build a Blog Assignment ----

# *** Setup ***
from flask import Flask, request, redirect, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:myblog@localhost:8889/blogz'
app.secret_key = 'ioga;skebr'  # for flash messages
db = SQLAlchemy(app)    # creating the database object

print('***TEST-1***')
# **** Begin Content ****

# Database Class Constructor
class Blog(db.Model):

    # Table Structure
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # constuctor
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    # Table Structure
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner') # relationship

    # constuctor
    def __init__(self, username, password):
        self.username = username
        self.password = password        


print('***TEST-2***')


# Log In
@app.route('/login', methods=['POST', 'GET'])
def login():
       
    # test if there is a 'POST' request
    if request.method == 'POST':

        # Get parameters from post request
        username = request.form['username_f']
        password = request.form['password_f']
        user = User.query.filter_by(username=username).first() 
        
        # Verification
        if user == None:                                # username does not exist
            flash('Username does not exist', 'user')
            return render_template('login.html')   
        elif not (user.password == password):           # password does not match
            flash('User password incorrect', 'pwd')
            return render_template('login.html')
        else:                                           # pass
            session['username'] = username              # store username in session
            return redirect('/blog')                        # return user to homepage when

    return render_template('login.html')


print('***TEST-3***')
# New Post Function
@app.route('/newpost', methods=['GET','POST'])
def newpost():
    
    
    # render this block of code when submit button is pressed
    if request.method == 'POST':
        
        # retrieve variables from form
        title = request.form['title_f']
        body = request.form['body_f']

        # Validatation: write error messages for empty text boxes
        if request.form['title_f'] == '':
            errorT = 'Please fill in the title'
        else:
            errorT = ''
        if request.form['body_f'] == '':
            errorB = 'Please fill in the body'
        else:
            errorB = ''


        # if there are error messages redisplay newpost page with errors
        if errorB or errorT :
            return render_template('newpost.html',errorTitle=errorT,errorBody=errorB,title_p=title,body_p=body)
        # if no error message redirect back to blog page
        else:
            # get form variables, save them
            entry_title = request.form['title_f']
            entry_body = request.form['body_f']
            
            # hit the session for current logged in user
            user = session['username']
            # hit the database for user id
            #user_id = User.query.filter_by(username=user)first()
            # database insertion
            blog_entry = Blog(entry_title, entry_body, user)
            db.session.add(blog_entry)
            db.session.commit()


            # get id of most recent blog entry
            value_id = blog_entry.id
            return redirect('/blog?id='+str(value_id))


    # render form when first loading page
    return render_template('newpost.html')


# Blog page Function
@app.route('/blog', methods=['GET'])
def index():


    # retrieve from url
    value_id = request.args.get('id')
    
    # test for presense of id in URL
    if value_id == None:
        value = False
    else:
        value = True

    if not value:
        # retrieve from database
        blog = Blog.query.all()
        return render_template('blog.html',blog=blog,value=value)
    else:
        value = True
        blog_x = Blog.query.filter_by(id=value_id).all()
        return render_template('blog.html',blog=blog_x,value=value)


# *** End Content ***

if __name__ == '__main__':
    app.run()