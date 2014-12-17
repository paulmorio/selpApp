import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfa_website.settings')

import django
django.setup()

from real_fantasy_adventure_app.models import Avatar, MyQuest
from django.contrib.auth.models import User


def populate():
    # set number of users in the for loop range
    for number in range(1,101):
        test_user = add_user(("test_"+ str(number)))
        test_avatar = add_avatar(test_user, test_user.username)
        # 3 MyQuests are created for each avatar
        for i in range(0,3):
            add_myQuest(test_avatar, i)

    # Print out what we have added 
    for user in User.objects.all():
        avatar = Avatar.objects.get(user=user)
        for myQuest in MyQuest.objects.filter(avatar=avatar):
            print "User: {0} - Avatar: {1} - MyQuest: {2}".format(str(user), str(avatar), str(myQuest))

def add_user(username):
    user = User.objects.create_user(username=username, email="test@test.com", password="test1234")
    return user

def add_avatar(user, nickname):
    avatar = Avatar.objects.get_or_create(user=user, nickname=nickname, bio=("Test Biography for " + nickname))
    return avatar

def add_myQuest(avatar, count):
    myQuest = MyQuest.objects.get_or_create(avatar=avatar[0], title="TestTitle" + "-" + str(count) + "_" + avatar[0].nickname, description="TestDesc" + str(count))
    return myQuest

# Start execution here!
if __name__ == '__main__':
    print "Starting RFA population script..."
    populate()