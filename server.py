'''
Created on 15.08.2014

@author: christoph
'''

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_wtf import Form

from wtforms.fields.simple import SubmitField, HiddenField

import os
from datetime import datetime
import random

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = '169d7c24b62bb17eafcc2bcded23e888'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


##Database Model Definition

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Float, default=1500.00)
    wins = db.Column(db.Integer, default=0)
    matches = db.Column(db.Integer, default=0)
    imgurl = db.Column(db.String(254))
    added = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return "<Player %s>" % self.id


##Views

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    buttonForm = ButtonForm()
    
    #load 2 different, random players from db
    player_context = [__get_random_player(), __get_random_player()]
    while player_context[0] is player_context[1]:
        player_context[1] = __get_random_player()
        
    if buttonForm.is_submitted():
        choice = buttonForm.choice.data
        choosen_player = player_context[choice-1]
        print "user voted", choosen_player
        
    return render_template('main.html', players=player_context, form=buttonForm)

def __get_random_player():
    rand = random.randrange(0, Player.query.count())
    return Player.query.get(rand)

@app.route("/ranking")
def ranking():
    #top_ten = sorted(players, key=lambda x: x.score, reverse=True)[0:10]
    top_ten = Player.query.order_by(Player.score).limit(10).all()22
    return render_template('ranking.html', players=top_ten)

@app.route("/player/<name>")
def player_details(name):
    #player = filter(lambda x: x.id == player_id, players)[0]
    player = Player.query.filter_by(name=name)
    return render_template('overview.html', player=player)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="sorry, your are wrong: %s" % e, code=404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e, code=500), 500



## Forms

class ButtonForm(Form):
    choice = HiddenField("choice")
    submit = SubmitField("Vote")
    


    

#for debugging only
def make_shell_context():
    return dict(app=app, db=db, Player=Player)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
    #app.run()
    