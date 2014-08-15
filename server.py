'''
Created on 15.08.2014

@author: christoph
'''
from elo_rating import Player

from flask import Flask, render_template

app = Flask(__name__)

players = [Player("foobar"), Player("Kunis")]


@app.route("/")
def mainpage():
    return render_template('main.html', players=players )



if __name__ == '__main__':
    app.run(debug=True)