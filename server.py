'''
Created on 15.08.2014

@author: christoph
'''
from elo_rating import Player

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def mainpage():
    players = [Player("foobar"), Player("Kunis")]
    return render_template('main.html', players=players )



if __name__ == '__main__':
    app.run(debug=True)