# user.py
from post import *
from follow import *
from newsfeed import *


def signup(db):

    while True:
        print("Please stroke 'enter' key to quit")
        id = input("id: ") # id
        if id == "":
            return False

        if not db.users.find_one({"id": id}): # if this id is not in users collection,

            while True:

                pw = input("pw: ") # password
                if pw == "":
                    return False

                if not re.match('^(?=.*?\d)(?=.*?[a-zA-Z])(?=.*?[!@#$%^&*()_+=-`~])[!@#$%^&*()_+=-`~A-Za-z\d]{8,}$', pw): # password restriction
                    print("Minimum 8 characters with at least one letter, one number and one special character.")
                    continue
                break

            name = input("name: ") # name
            if name == "":
                return False

            birthday = input("birthday(YYMMDD)") # birthday
            if birthday == "":
                return False

            if '-' in birthday:
                birthday = "".join(birthday.split('-')) # get rid of '-' from user's input

            phone = input("phone number: ") # phone number
            if phone == "":
                return False

            if '-' in phone:
                phone = "".join(phone.split('-')) # get rid of '-' from user's input

            print("You signed up with ", id, pw, name, birthday, phone,"\n")
            db.users.insert_one({"id": id, "pw": pw, "name": name, "birthday": birthday,\
                                 "phone":phone, "following":[], "followers":[]})

            return False

        print("The ID already exists. Please try another ID!\n")


def signin(db):

    while True:

        print("\nPlease Login! Please stroke 'enter' key to quit")
        id = input("Please input your ID: ")
        if id == "":
            return False

        if not db.users.find_one({"id":id}):
            print("There is no ID like this.\n")
            continue


        else:
            pw = input("Please input your password:")
            if pw == "":
                return False

            if not db.users.find_one({"pw":pw}):
                print("Wrong Password!\n")
                continue

            print("Login success!\n")
            # document = db.users.find_one({"id": id, "pw": pw})
            # userpage(db, id, document)
            userpage(db, id)


# def userpage(db, id, document):
def userpage(db, id):
    x = PrettyTable()
    x.field_names = ["no", "function"]
    x.add_row(["1", "Status message"])
    x.add_row(["2", "Following and follower list"])
    x.add_row(["3", "Follow & Unfollow"])
    x.add_row(["4", "My posting"])
    x.add_row(["5", "Newsfeed"])
    x.add_row(["0", "Quit"])

    switcher = {1: changeStatus,
                2: followList,
                3: followOrUnfollow,
                4: posting,
                5: newsfeed,
                0: exit}

    while True:
        print("\nWelcome to", id + "'s userpage!")
        print(x)
        document = db.users.find_one({"id": id})
        task_no = input("What do you want to do here? Please enter the task's number: \n")
        selected_task = switcher.get(int(task_no), print_wrong)
        if selected_task == exit:
            exit()
        selected_task(db, id, document)


def confirm(db, id, curr_status):
    confirm = input("\nDo you want to change your status?(y/n):")

    if confirm in ["Y", "y", "yes", "Yes", "YES"]:
        new_status = input("Enter new status: ")
        db.status.insert_one({'id': id, 'status': new_status})
        if curr_status:
            db.status.delete_one({'id': id})


    elif confirm in ["N", "n", "no", "NO", "No"]:
        pass

    else:
        print("\nWrong input!")


def changeStatus(db, id, document):

    curr_status = db.status.find_one({'id':id})

    if curr_status:
        print("\n'{}'".format(curr_status['status']))
        confirm(db, id, curr_status)

    else:
        print("\nYou have no status message now!")
        confirm(db, id, curr_status)


def followList(db, id, document):

    followings = document["following"]
    followers = document["followers"]
    print(id + " has", len(followings), "followings,", len(followers), "followers")

    want_to_see_list = input("\nDo you want to see people's list?(y/n):")
    if want_to_see_list in ["Y","y","yes","Yes","YES"]:
        print("followings:", followings,"\nfollowers:", followers)


