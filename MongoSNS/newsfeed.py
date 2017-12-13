import pymongo
from prettytable import PrettyTable
import numpy as np
import codecs, json


def newsfeed(db, id, document):

    ids = db.users.find_one({'id':id})['following']
    ids.append(id)
    posts = db.posts.find({'id': {'$in': ids}}).sort('reference', -1).limit(10)

    x = PrettyTable()
    x.field_names = ["ID", "Post", "Time"]
    for post in posts:
        x.add_row([post['id'],post['post'], str(post['year']) + "/" + str(post['month']) + '/' + str(post['day']) + " " \
                   + str(post['hour']) + ":" + str(post['minute']) + ':' + str(post['second'])])

    print(x)



"""
It is similar to the function in wall.py
Get posts of your followings.
There can be a few options to sort the posts such as posting date or alphabetical order of following's name.
"""
