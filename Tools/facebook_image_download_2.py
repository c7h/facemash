'''
Created on 16.08.2014

Download all the images from facebook-group users.
Ugglyy Hack, but works! (but is possible insecure - better run in in a save environment)
1. obtain an ACCESS TOKEN from Facebook:
   https://developers.facebook.com/tools/explorer
2. set the 'target' GROUP ID
   ...just read it from the URI

wget needed!
@author: Christoph Gerneth
'''

from urllib2 import urlopen
import json
import os
import sys

# ----SETTINGS!----
group_id = 494276867251269
access_token = "CAACEdEose0cBAG0ZCic3bOPpgWazFZBeoq4nJ2oEh4YmJ0pz6DSLcmIWkZAvlR8Bllh7xLi9GupqZC7VtiZCInjETK3ZBBANsKEaDDn7lrZBiys0lcBbYWASZC5mbKF5kFk09ud4ZBOpffSKq5PViiZBMMfWrdunTR9pQsVIecgLTuQhLZCiq1ew3Ia8inwwqOTjQRTbZCDM9GPSjlwVABdJ967g"
WIDTH = 480
HEIGHT = 480
#--------END--------


class Member(object):
    def __init__(self, name, id, admin=False):
        self.name = name
        self.id = id
        self.admin = admin

    def __repr__(self):
        return "<User %s>" % self.name


def make_request(group_id, access_token):
    url = "https://graph.facebook.com/v2.1/%i/members?access_token=%s" % (group_id, access_token)
    print url

    request = urlopen(url)
    req_string = request.read()
    return req_string

def create_members(group_json):
    members = []
    for member in group_json['data']:
        mem = Member(member['name'], member['id'], admin=member['administrator'])
        members.append(mem)
    return members

def get_img_for_user(user_id, user_name=None, width=WIDTH, height=HEIGHT):
    request_url = "https://graph.facebook.com/v2.1/%s/picture?width=%i&height=%s&redirect=false" % (user_id, width, height)
    req = urlopen(request_url)
    json_data = req.read()
    di = json.loads(json_data)
    url = di['data']['url']
    img_name = unicode(user_name.lower().replace(" ", "_")+".jpg")
    #build your download command
    sys.stdout.write("foo %s" % img_name.encode('utf-8'))
    command = 'wget %s -O %s' % (url.encode('utf-8'), img_name.encode('utf-8'))
    print command
    os.system(command)

try:
    req_string = make_request(group_id, access_token)
except Exception, e:
    print "[ERROR]", e
    sys.exit()

user = json.loads(req_string)
members = []
members.extend(create_members(user))


print "found %i users in group" % len(members)
if raw_input("proceed? (y/n)") == "n":
    sys.exit()

#aaaand download
for member in members:
    get_img_for_user(member.id, member.name, 500)

