# main.py
from user import *
from pymongo import MongoClient



client = MongoClient()
db = client.project

def mainpage(db):

    while True:
        sign = int(input("\nSign up or sign in?: \n"
                     "(Please enter 1 for sign up or 2 for sign in. 0 to quit)"))

        if sign == 1:
            signup(db)


        elif sign == 2:
            signin(db)


        elif sign == 0:
            exit()

        else:
            print("Wrong input! Please enter 1 or 2\n")


if __name__ == "__main__":
    mainpage(db)
