import re
from prettytable import PrettyTable

def posting(db, id, document):
    x = PrettyTable()
    x.field_names = ["Post_num", "ID", "Post", "Time"]

    posts = db.posts.find({'id': id})
    for post in posts:
        x.add_row([post['post_num'], id, post['post'], str(post['year'])+"/"+str(post['month'])+'/'+str(post['day']) +" "\
                   +str(post['hour'])+":"+str(post['minute'])+':'+str(post['second'])]) # post number 어떻게 가져올지 생각해보자.

    print(x)

    task = input("1: Insert post, 2: Delete post, 3: Tag search, 0: quit: ")
    if task == "1":
        insertPost(db, id)

    elif task == "2":
        deletePost(db, id)

    elif task == "3":
        tagSearch(db, id)

    elif task == "0":
        pass

    else:
        print_wrong()


def insertPost(db, id):
    import time
    post_num = db.posts.find({'id': id}).count() + 1
    post = input("Write post here: ")
    tag = input("Any hash tags? If you don't have just press 'Enter'.: ")
    tags = [x.strip("#") for x in tag.split()]

    post_time = time.localtime(time.time())
    db.posts.insert_one({"post_num": post_num, "id": id, 'post': post, 'year': post_time[0], 'month': post_time[1],\
                        'day': post_time[2], 'hour': post_time[3], 'minute': post_time[4], 'second': post_time[5],\
                         'reference':time.time(), 'tags': tags})



def deletePost(db, id):
    want_to_delete_post = input("Which post do you want to delete? Please enter the post number: ")
    pw_verification = input("Please enter your password again: ")
    real_pw = db.users.find_one({'id':id})['pw']

    if pw_verification == real_pw:
        confirm = input("Are you sure to delete post number{}?(y/n):".format(want_to_delete_post))

        if confirm in ["Y","y","yes","Yes","YES"]:
            db.posts.delete_one({'id': id, 'post_num': int(want_to_delete_post)})

        elif confirm in ["N", "n", "no", "NO", "No"]:
            pass

        else:
            print("Wrong input!")


def tagSearch(db, id):
    tag = input("Please enter a tag what you want to search!: ").strip("#")

    x = PrettyTable()
    x.field_names = ["#{}".format(tag), "ID", "Post", "Time"]

    posts = db.posts.find({'tags':{"$elemMatch":{'$eq': tag}}})
    if posts.count() == 0:
        print("There is no post matching for '{}'!".format(tag))

    else:
        for post in posts:
            x.add_row([post['post_num'], id, post['post'],
                       str(post['year']) + "/" + str(post['month']) + '/' + str(post['day']) + " " \
                       + str(post['hour']) + ":" + str(post['minute']) + ':' + str(
                           post['second'])])  # post number 어떻게 가져올지 생각해보자.

        print(x)


def print_wrong():
    print("\nwrong menu number.")
