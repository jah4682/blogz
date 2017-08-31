# ---- Build a Blog Assignment ----

# *** Setup ***
from flask import Flask, request, redirect, render_template, flash, request, session
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
       
    if request.method == 'POST':                        # if form is submitted

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
            return redirect('/blog')                    # return user to main blog page

    return render_template('login.html')                # first load page render blank form


print('***TEST-3***')


# Signup
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == 'POST':

        # request form information
        username = request.form['username_f']
        pwd = request.form['password_f']
        verify = request.form['verify_f']

        # if user exist get record from database
        user = User.query.filter_by(username=username).first()
        if user != None:
            print(user.username)

        # Validate Username
        if user != None:                                            # if not in database skip inner if to avoid error
            if user.username == username:                           # if exist
                flash('this username already exists')
                
        elif username == '':                                        # if field left blank
            flash('username must be filled in')
            
        elif ' ' in username:                                       # if space
            flash('username cannot contain a space')
            
        elif len(username) < 3 or len(username) > 20:               # if out of range 3 to 20
            flash('username must be between 3 and 20 characters long')
            
        # Validate Password
        elif pwd == '':                                             # if field left blank
            flash('password must be filled in', 'blank')
            
        elif ' ' in pwd:                                            # if space
            flash ('password cannot contain a space', 'space')
            
        elif len(pwd) < 3 or len(pwd) > 20:                         # if out of range 3 to 20
            flash('password must be between 3 and 20 characters long', 'range')
            
        # validate password confirmation
        elif not (pwd == verify):
            flash('your passwords do not match', 'match')
            return render_template('signup.html')

        # if successful add new user to database and redirect user to newpost page
        else:
            new_user = User(username, pwd)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')


    return render_template('signup.html')


print('***TEST-4***')


# log Out
@app.route('/logout')
def logout():
    print(session)
    if session:
        del session['username'] # delete username from session
    return redirect('/blog')


print('***TEST-5***')


# Pages to be viewed without a Log in
@app.before_request
def require_login():
    allowed_routes = ['index','login', 'list_blogs', 'signup', 'logout']    # name of functions, not URL routes

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

print('***TEST-6***')

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
            user_id = User.query.filter_by(username=user).first()
            # database insertion
            blog_entry = Blog(entry_title, entry_body, user_id)
            db.session.add(blog_entry)
            db.session.commit()


            # get id of most recent blog entry
            value_id = blog_entry.id
            return redirect('/blog?id='+str(value_id))


    # render form when first loading page
    return render_template('newpost.html')

print('***TEST-7***')


# Blog page Function
@app.route('/blog', methods=['GET'])
def list_blogs():


    # retrieve from url, returns None if url has no query string.
    value_id = request.args.get('id')                               
    value_user = request.args.get('user')
    print("******what bool is this?****",bool(value_user),"  user Id -  ",value_user)
    print("******what bool is this?****",bool(value_id),"  title id -  ",value_id) # is None false?
    

    # Boolean Variables
    '''if value_id == None and value_user == None:                     # test for presense of id in URL
        value_i = True
        value_u = True
    elif value_id == None and value_user:
        value_i = False
        value_u = True
    else:
        value_i = True
        value_u = False'''
    #value_u = False

    # Boolean test: Which interior setup to render?
    if value_user:
        # list user page   

        user_blogs = Blog.query.filter_by(owner_id=value_user).all()
        print('****query database test*****',user_blogs)
        return render_template('blog.html',user=user_blogs,value_u=value_user)

    elif value_id:
        # individual blog   
       
        blog_x = Blog.query.filter_by(id=value_id).all()
        return render_template('blog.html',blog=blog_x,value_i=value_id)        

    else:       
        # list all blog titles
        blogs = Blog.query.all() # retrieve from database
        # print('****query database test*****',blogs[0].owner.id)
        return render_template('blog.html',blogs=blogs)        
        # ,value_i=value_i,value_u=value_u
        
        
        


print('***TEST-8***')

# Home page. List of users.
@app.route('/')
def index():

    users = User.query.all()
    return render_template('index.html', users=users)

print('***TEST-9***')
# *** End Content ***

if __name__ == '__main__':
    app.run()