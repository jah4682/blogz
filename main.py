# ---- Build a Blog Assignment ----

# *** Setup ***
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:myblog@localhost:8889/build-a-blog'


db = SQLAlchemy(app)    # creating the database object


# **** Begin Content ****

# Database Class Constructor
class Blog(db.Model):

    # Table Structure
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


# New Post Function
@app.route('/newpost', methods=['GET','POST'])
def newpost():
    print('**TEST***')
    
    # render this block of code when submit button is pressed
    if request.method == 'POST':
        # retrieve variables
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
            # get from form
            entry_title = request.form['title_f']
            entry_body = request.form['body_f']
            
            # database insertion
            blog_entry = Blog(entry_title, entry_body)
            db.session.add(blog_entry)
            db.session.commit()

            return redirect('/blog')


    # render form when first loading page
    return render_template('newpost.html')


# Blog page Function
@app.route('/blog', methods=['GET'])
def blog():

    # retrieve from database
    blog = Blog.query.all()
    print(blog)
    return render_template('blog.html',blog=blog)



# *** End Content ***

if __name__ == '__main__':
    app.run()