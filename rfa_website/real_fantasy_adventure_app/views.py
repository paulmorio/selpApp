from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from real_fantasy_adventure_app.models import Quest, Avatar, MyQuest
from real_fantasy_adventure_app.forms import AvatarForm, UserForm, MyQuestForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):

    # make a list of the top 5 players by points
    avatars_by_academic = Avatar.objects.order_by('-num_academic_points')[:5]
    avatars_by_professional = Avatar.objects.order_by('-num_professional_points')[:5]
    avatars_by_athletic = Avatar.objects.order_by('-num_athletic_points')[:5]

    # make a context dictionary for each
    context_dict = {'academics': avatars_by_academic, 'professionals': avatars_by_professional, 'athletes': avatars_by_athletic}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'real_fantasy_adventure_app/index.html', context_dict)

def about(request):
	context_dict = {'boldthing' : "You are an adventurer"}

	return render(request, 'real_fantasy_adventure_app/about.html', context_dict)

def notLoggedIn(request):
    return render(request, 'real_fantasy_adventure_app/notLoggedIn.html')

# @login_required(login_url='/real_fantasy_adventure_app/notLoggedIn/')
def avatarProfile(request, avatar_name_slug):
    context_dict = {}

    # find out the identity of the visitor making the request
    current_user = request.user

    try:
        # Can we find a avatar nickname slug with the given nickname?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        avatar = Avatar.objects.get(slug=avatar_name_slug) 

    except Avatar.DoesNotExist:
        # the template displays the "no avatar" message
        pass

    context_dict['avatar'] = avatar
    context_dict['avatar_name'] = avatar.nickname
    context_dict['avatar_name_slug'] = avatar_name_slug
    context_dict['avatar_bio'] = avatar.bio
    context_dict['avatar_level'] = avatar.level
    context_dict['avatar_num_professional_points'] = avatar.num_professional_points
    context_dict['avatar_num_athletic_points'] = avatar.num_athletic_points
    context_dict['avatar_num_academic_points'] = avatar.num_academic_points
    context_dict['avatar_created_date'] = avatar.created_date

    # if the avatar belongs to the current user we show him all of the attributes of his avatar,
    # his/her myQuests and the myQuest button
    if (avatar.user == current_user):
        # set a variable that is will be used to between the cases
        is_users_avatar = avatar.nickname
        context_dict['is_users_avatar'] = is_users_avatar
        # Retrieve all of the associated myQuests.
        # Note that filter returns >= 1 model instance.
        myQuests = MyQuest.objects.filter(avatar=avatar)
        # Adds our results list to the template context under nickname myQuests.
        context_dict['myQuests'] = myQuests

        return render(request, 'real_fantasy_adventure_app/avatarProfile.html', context_dict)

    # if the current user is looking at someone else's avatar they can simply look at their 
    # avatar specs without the myQuests as they are private.
    else:
        # Go render the response and return it to the client.
        return render(request, 'real_fantasy_adventure_app/avatarProfile.html', context_dict)

def register(request):
    #boolean variable that controls whether registrations was successful or not
    registered = False

    if (request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        avatar_form = AvatarForm(data=request.POST)

        if user_form.is_valid() and avatar_form.is_valid():
            user = user_form.save()

            # now we hash the password
            user.set_password(user.password)
            user.save()

            # now we work on the avatar
            avatar = avatar_form.save(commit=False)
            avatar.user = user

            # save the avatar model instance
            avatar.save()

            # finally set our registration to be complete
            registered = True

        # There were problems during the registration process
        else:
            print user_form.errors, avatar_form.errors            

    # the request method was not of type POST and therefore we show black forms ready for input
    else: 
        user_form = UserForm()
        avatar_form = AvatarForm()

    # render depending on the context
    return render(request, 'real_fantasy_adventure_app/register.html', {'user_form': user_form, 'avatar_form': avatar_form, 'registered': registered})

def user_login(request):

    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        # the authenticate method returns a user object if the credentials exist within the database
        user = authenticate(username=username, password=password)

        if user:
            # is the user active?
            if user.is_active:
                # if the account is active and credentials match we login the user
                login(request,user)
                return HttpResponseRedirect('/real_fantasy_adventure_app/')
            else:
                # an inactive account was used so login shouldnt be possible
                return HttpResponse('This account has been deactivated')
        else:
            # login credentials were incorrect
            print "Invalid login credentials: {0}, {1}".format(username, password)
            return HttpResponse('Invalid login credentials')

    else:
        # the request method was not of type POST, thus we show the login forms
        return render(request, 'real_fantasy_adventure_app/login.html', {})

@login_required(login_url='/real_fantasy_adventure_app/')
def user_logout(request):
    # since the check if logged in is done beforehand we can just log the user out
    logout(request)
    return HttpResponseRedirect('/real_fantasy_adventure_app/')

def add_myQuest(request, avatar_name_slug):
    try:
        avatar = Avatar.objects.get(slug=avatar_name_slug)
    except Avatar.DoesNotExist:
        avatar = None

    if (request.method == 'POST'):
        form = MyQuestForm(request.POST)
        if form.is_valid():
            if avatar:
                    myQuest = form.save(commit=False)
                    myQuest.avatar = avatar
                    myQuest.save()
                    # probably better to use a redirect here.
                    return avatarProfile(request, avatar_name_slug)
            else:
                print form.errors
    else:
        form = MyQuestForm()
        context_dict = {'form': form, 'avatar': avatar, 'avatar_name_slug': avatar_name_slug}

    return render(request, 'real_fantasy_adventure_app/add_myQuest.html', context_dict)





