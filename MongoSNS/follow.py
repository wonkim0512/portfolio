from pymongo.errors import ConnectionFailure
import sys
import re

def followOrUnfollow(db, id, document):
    select = int(input("which function do you want to do? enter 1 to follow or enter 2 to unfollow?: "))

    if select == 1:
        follow(db, id, document)

    elif select == 2:
        unfollow(db,id,document)

    else:
        print("Wrong input!")

def follow(db, id, document):
    try:

        want_to_follow_id = input("Enter the id which you want to follow: ")
        if not db.users.find_one({'id': want_to_follow_id}):
            print("There is not id '{}'".format(want_to_follow_id))

        else:
            if id == want_to_follow_id:
                print("You cannot follow yourself!")

            else:
                if want_to_follow_id in db.users.find_one({'id':id})['following']:
                    print("You already follow him/her.")

                else:
                    db.users.update({'id': id}, {'$addToSet': {'following': want_to_follow_id}})
                    db.users.update({'id': want_to_follow_id}, {"$addToSet":{'followers': id}})
                    print("Following done!")


        '''
        1. 팔로우하고자 하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 있으면 경고 출력

        3. 팔로잉 목록에 없으면,
            나의 팔로잉 목록에 팔로우할 유저id 추가 + 상대방의 팔로워 목록에 내 id 추가
        '''

    except Exception as e:
        sys.stderr.write("could not operate following %s\n" %e)

def unfollow(db, id, followid):
    try:
        want_to_unfollow_id = input("Enter the id which you want to unfollow: ")
        if id == want_to_unfollow_id:
            print("You cannot unfollow yourself!")


        else:
            if want_to_unfollow_id in db.users.find_one({'id':id})["following"]:
                db.users.update({'id':id}, {"$pull": {'following': want_to_unfollow_id}})
                db.users.update({'id': want_to_unfollow_id}, {"$pull":{"followers": id}})

            else:
                print("You have not been following {}".format(want_to_unfollow_id))


        '''
        1. 언팔로우하고자하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 언팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 없으면 경고 출력

        3. 팔로잉 목록에 있으면,
            나의 팔로잉 목록에서 언팔로우할 유저id 제거 + 상대방의 팔로워 목록에서 내 id 제거
        '''
    except Exception as e:
        sys.stderr.write("could not operate following %s\n" %e)
