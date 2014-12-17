import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfa_website.settings')

import django
django.setup()

from real_fantasy_adventure_app.models import Avatar, MyQuest
from django.contrib.auth.models import User

num_users_and_avatars_to_create = 100
num_myquests_to_create_for_avatar = 3

def populate():
    """
    Uses the functions add_user, add_avatar, add_myQuest to populates the database with a number
    of unique users/avatars specified by num_users_and_avatars_to_create global variable, and 
    number of MyQuests to create for each avatar controlled by num_myquests_to_create_for_avatar
    global variable.

    Prints out the Users, Avatars, and MyQuests created onto the CLI

    Making more than 10000 users can take a while so it is recommended to run this script in
    another screen.

    Warning: Due to warnings described below, it would be best delete all test users that were 
        created by this population script before. ie. any users who have the name following this
        pattern: "test_i" where "i" is any number between 1 and num_users_and_avatars_to_create.
        This is due to there not being a get_or_create() function for User instances unlike the
        Avatar and MyQuest models.
    """
    # set number of users in the for loop range
    for number in range(1, num_users_and_avatars_to_create+1):
        test_user = add_user(("test_"+ str(number)))
        test_avatar = add_avatar(test_user, test_user.username)
        # 3 MyQuests are created for each avatar
        for i in range(0, num_myquests_to_create_for_avatar+1):
            add_myQuest(test_avatar, i)

    # Print out what we have added 
    for user in User.objects.all():
        avatar = Avatar.objects.get(user=user)
        for myQuest in MyQuest.objects.filter(avatar=avatar):
            print "User: {0} - Avatar: {1} - MyQuest: {2}".format(str(user), str(avatar), str(myQuest))

def add_user(username):
    """Creates a test user given a username, with email=test@test.com and password = test1234"""
    user = User.objects.create_user(username=username, email="test@test.com", password="test1234")
    return user

def add_avatar(user, nickname):
    """
    Gets an avatar and returns it if matching user is found based on its user, and nickname, or creates
    a new avatar with the paramaters provided

    Warning: Database level exceptions occur if the one to one relationship between avatars and users is violated
    Warning: Database level Integrity Errors occur if any of the uniqueness constraints are violated (ie nickname as example)
    """
    avatar = Avatar.objects.get_or_create(user=user, nickname=nickname, bio=("Test Biography for " + nickname))
    return avatar

def add_myQuest(avatar, count):
    """
    Gets an MyQuest and returns it if matching user is found based on its user, and nickname, or creates
    a new MyQuest with the paramaters provided

    Warning: Database level exceptions occur if the many to one relationship between MyQuest and Avatar is violated
    Warning: Database level Integrity Errors occur if any of the uniqueness constraints are violated (ie slug as example)
    """
    myQuest = MyQuest.objects.get_or_create(avatar=avatar[0], title="TestTitle" + "-" + str(count) + "_" + avatar[0].nickname, description="TestDesc" + str(count))
    return myQuest

# Start execution here!
if __name__ == '__main__':
    print "Starting RFA population script..."
    populate()