'''
Created on 16.08.2014
Migration helper...

put all your images in the static/face/ directory in format "forename_lastname.jpg"

@author: Christoph Gerneth
'''
import sys
import os
sys.path.append("../")
from server import Player, db


gifs = os.listdir("../static/face/")


db.drop_all()
db.create_all()

print gifs

for fn in gifs:
    name = fn.split(".")[0]
    name = name.split("_")
    name_cap = map(str.capitalize, name)
    obj = Player(name=" ".join(name_cap).decode('utf-8'), imgurl=fn.decode("utf-8"))
    db.session.add(obj)
    
db.session.commit()

    
