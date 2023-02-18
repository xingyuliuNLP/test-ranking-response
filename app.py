import os
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.static_folder = 'static'

## database setting ##
# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')
app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Cands(db.Model):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    question = Column(String(8000))
    answer = Column(String(8000))

class Result(db.Model):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    commentaire = Column(String(8000))
    answer = Column(String(8000))

## database setting ##


def return_responses(q):
    cands = Cands.query.filter_by(question=q).all()
    response=[]
    for cand in cands:
        response.append(cand.answer)
    return response

@app.route("/", methods=['GET', 'POST'])
def expert():
    cands=Cands.query.all()
    return render_template("index.html", cands=cands)

@app.route('/add', methods=['POST'])
def add_commentaire():
    response = request.values.get('response')
    commentaire = request.values.get('commentaire')
    result=Result()
    result.commentaire = commentaire
    result.answer = response
    db.session.add(result)
    db.session.commit()

@app.route("/get_response/")
def get_bot_response():
    question = request.args.get('msg')
    rs=return_responses(question)
    return rs

if __name__ == "__main__":
    app.run()
