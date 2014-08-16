'''
Created on 15.08.2014

@author: christoph
'''

from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_wtf import Form

from wtforms.fields.simple import SubmitField, HiddenField

from elo import Elo

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
elo = Elo()

##Database Model Definition

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Unicode(64), nullable=False)
    score = db.Column(db.Float, default=1500.00)
    wins = db.Column(db.Integer, default=0)
    matches = db.Column(db.Integer, default=0)
    imgurl = db.Column(db.Unicode(254))
    added = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return "<Player %s>" % self.id

##Views

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    buttonForm = ButtonForm()
    
    #load 2 different, random players from db - first one with less matches
    player_context = [__get_random_player(match_treshold=35), __get_random_player()]
    while player_context[0].id == player_context[1].id:
        player_context[1] = __get_random_player()
    
    if session.new:
        session['player_store'] = [x.id for x in player_context]
    
    if buttonForm.is_submitted():
        choice = int(buttonForm.choice.data)
        winner_id = session['player_store'][choice-1]
        looser_id = session['player_store'][choice-2]
        
        winner = Player.query.get(winner_id)
        looser = Player.query.get(looser_id)
        
        print "[USER VOTED]: winner %s - looser: %s" % (winner, looser)
        winner, looser = elo.match(winner, looser)
        db.session.commit()
    
    session['player_store'] = [x.id for x in player_context]


    return render_template('main.html', players=player_context, form=buttonForm)

def __get_random_player(match_treshold=None):
    '''load a random player from database. 
    match_treshold is between 0 and 100.'''
    count = Player.query.count()
    if match_treshold:
        rand = random.randint(0, int(count*0.01*match_treshold))
        pl = Player.query.order_by(Player.matches.asc())[rand]
    else:
        rand = random.randrange(1, count+1)
        pl = Player.query.get(rand)
    
    return pl

@app.route("/ranking/<int:limit>")
def ranking(limit):
    limit = min(limit, 100)
    top = Player.query.order_by(Player.score.desc()).limit(limit).all()
    return render_template('ranking.html', players=top)

@app.route("/player/<id>")
def player_details(id):
    player = Player.query.filter_by(id=id).first()
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
    #app.run(debug=True)
    