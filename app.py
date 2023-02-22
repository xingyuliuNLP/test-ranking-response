import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    username = Column(String(50))
    question = Column(String(8000))
    answer = Column(String(8000))
    sourceq = Column(String(50))
    thematique = Column(String(50))

    def __str__(self):
        return self.name
class results(db.Model):
    __tablename__ = 'results'
    username = Column(String(50),primary_key=True)
    rchosen = Column(String(8000))
    rmodified = Column(String(8000))
    comment = Column(String(8000))

## database setting ##


@app.route("/", methods=['GET', 'POST'])
def expert():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add_commentaire():
    colis = request.get_json()
    user = colis['user']
    rchosen = colis['rChosen']
    response = colis['rModified']
    commentaire = colis['cmt']
    result=results()
    result.username = user
    result.comment = commentaire
    result.rmodified = response
    result.rchosen = rchosen
    db.session.add(result)
    db.session.commit()

@app.route("/newquestion",methods=['POST'])
def newquestion():
    colis = request.get_json()
    print(colis)
    cands=Cands.query.filter_by(username=colis).all()
    response={}
    r=[]
    q=[]
    for cand in cands:
        q.append(cand.question)
        r.append(cand.answer)
    response['q']=q[0]
    response['r']=r
    return jsonify(response)

if __name__ == "__main__":
    app.run()
