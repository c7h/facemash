'''
Created on 15.08.2014

@author: christoph
'''
from elo_rating import Player

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import Form
from wtforms.fields.simple import SubmitField, HiddenField

import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = '169d7c24b62bb17eafcc2bcded23e888'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#prototype:
players = [Player("foobar", image_url="http://assets.nydailynews.com/polopoly_fs/1.1258231.1360341394!/img/httpImage/image.jpg_gen/derivatives/article_970/s13-vday.jpg"), 
           Player("Kunis", image_url="http://cdn01.cdnwp.celebuzz.com/wp-content/uploads/2013/08/13/mila-kunis-2.gif"),
           ]

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    buttonForm = ButtonForm()
    player_context = players[0:2] #@TODO: load 2 players from database
    
    if buttonForm.validate_on_submit():
        choice = buttonForm.choice.data
        choosen_player = player_context[choice-1]
        

    
    return render_template('main.html', players=player_context, form=buttonForm)


@app.route("/ranking")
def ranking():
    top_ten = sorted(players, key=lambda x: x.score, reverse=True)[0:10]
    return render_template('ranking.html', players=top_ten)

@app.route("/player/<player_id>")
def player_details(player_id):
    player = filter(lambda x: x.id == player_id, players)[0]
    print player
    return render_template('overview.html', player=player)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="sorry, your are wrong: %s" % e, code=404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e, code=500), 500

class ButtonForm(Form):
    choice = HiddenField("choice")
    submit = SubmitField("Vote")
    

##Database Model Definition

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.String(64), primary_key=True)
    score = db.Column(db.Float, default=1500.00)
    wins = db.Column(db.Integer)
    matches = db.Column(db.Integer)
    imgurl = db.Column(db.String(254))
    added = db.Column(db.DateTime, default=datetime.now())
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")