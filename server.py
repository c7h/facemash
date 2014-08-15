'''
Created on 15.08.2014

@author: christoph
'''
from elo_rating import Player

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

#prototype:
players = [Player("foobar", image_url="http://assets.nydailynews.com/polopoly_fs/1.1258231.1360341394!/img/httpImage/image.jpg_gen/derivatives/article_970/s13-vday.jpg"), 
           Player("Kunis", image_url="http://cdn01.cdnwp.celebuzz.com/wp-content/uploads/2013/08/13/mila-kunis-2.gif")]

@app.route("/")
def mainpage():
    return render_template('main.html', players=players)


@app.route("/ranking")
def ranking():
    top_ten = sorted(players, key=lambda x: x.score, reverse=True)[0:10]
    return render_template('ranking.html', players=top_ten)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="sorry, your are wrong: %s" % e, code=404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e, code=500), 500

if __name__ == '__main__':
    app.run(debug=True)