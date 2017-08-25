# ---- Build a Blog Assignment ----

# *** Setup ***
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLACHEMY_ECHO'] = True
app.config['SQLACHEMY_DATABASE_URI'] = mysql+pymysql:build-a-blog:myblog@@localhost:8889/build-a-blog'

db = SQLAlchemy(app)    # creating the database object


# *** Begin Content ***




# *** End Content ***

if __name__ == '__main__':
    app.run()