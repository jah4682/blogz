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
            return render_template('newpost.html',errorTitle=errorT,errorBody=errorB)
        # if no error message redirect back to blog page
        else:
            return redirect('/blog')


    # render form when first loading page
    return render_template('newpost.html')


# Blog page Function
@app.route('/blog', methods=['GET'])
def blog():

    
    return render_template('blog.html',title="Build a Blog")



# *** End Content ***

if __name__ == '__main__':
    app.run()