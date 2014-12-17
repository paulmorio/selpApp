from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from real_fantasy_adventure_app.models import Quest, Avatar, MyQuest
from real_fantasy_adventure_app.forms import AvatarForm, UserForm, MyQuestForm, StatChangeForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from real_fantasy_adventure_app.statChange import inc_professional_points, inc_athletic_points, inc_academic_points


# Create your views here.

def index(request):
    """
    View for the Index, a blank string after /real_fantasy_adventure_app/ in the URL redirects the user to this view,
     and its corresponding template
    """

    # make a list of the top 5 players by points
    avatars_by_academic = Avatar.objects.order_by('-num_academic_points')[:5]
    avatars_by_professional = Avatar.objects.order_by('-num_professional_points')[:5]
    avatars_by_athletic = Avatar.objects.order_by('-num_athletic_points')[:5]

    # make a context dictionary for each
    context_dict = {'academics': avatars_by_academic, 'professionals': avatars_by_professional, 'athletes': avatars_by_athletic}

    # do a quick check on the identity of the user so that we can decide whether they can
    # access their avatar profile.
    current_user = request.user
    if (current_user.is_authenticated()):
        avatar = Avatar.objects.get(user=current_user)
        context_dict['avatar_name_slug'] = avatar.slug 

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'real_fantasy_adventure_app/index.html', context_dict)

def about(request):
    """View for the about page"""
	context_dict = {'boldthing' : "You are an adventurer"}

	return render(request, 'real_fantasy_adventure_app/about.html', context_dict)

def notLoggedIn(request):
    """View function that handles cases where the notLoggedIn page must be shown"""
    return render(request, 'real_fantasy_adventure_app/notLoggedIn.html')

@login_required(login_url='/real_fantasy_adventure_app/notLoggedIn/')
def avatarProfile(request, avatar_name_slug):
    """
    This view handles the displaying of avatar profile pages and the available items depending on which 
    what kind of visitor attempts to view the avatar page

    There are 3 important cases
    1. The visitor is not logged in, thus he/she is redirected to the notLoggedIn page
    2. The visitor is logged in, but the avatar page visited is not his/her own avatar. In this
        case, hours cannot be logged, and myQuests cannot be viewed.
    3. The visitor is logged in and the avatar profile requested is the same as the users
        avatar. Thus the is_users_avatar variable is added to the context dictionary,
        so that everything is viewable
    """
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
    context_dict['avatar_total_points'] = avatar.get_total_points()

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
    """
    View handles the registration form, and communicates with the database to save
    the relevant model created by using UserForm and AvatarForm from the forms module
    """
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
    """
    This view handles the logging in of authenticated models, and checks for correctness 
    of credentials provided. The password hasher currently used is the standard one by 
    django (as of 1.7).
    """

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

@login_required(login_url='/real_fantasy_adventure_app/notLoggedIn/')
def user_logout(request):
    """View logs out the user if he/she is logged in"""
    # since the check if logged in is done beforehand we can just log the user out
    logout(request)
    return HttpResponseRedirect('/real_fantasy_adventure_app/')

@login_required(login_url='/real_fantasy_adventure_app/notLoggedIn/')
def myQuest(request, avatar_name_slug, myQuest_name_slug):
    """
    View handles requests to view myQuests of avatars. As the viewing of myQuests should 
    only be done by the avatar that owns the MyQuests both the avatar slug and the
    myquest slug are required to view the MyQuest and thus comprise the second and third
    parameter this function respectively.

    If the avatar's number of points in each of the categories exceeds the 
    req_<category>_points a congratulation is shown to the user, as well 
    as an additional congratulations if the avatar has exceeded in all categories
    """
    context_dict = {}
    current_user = request.user
    try:
        avatar = Avatar.objects.get(slug=avatar_name_slug)
    except Avatar.DoesNotExist:
        avatar = None
    try:
        myQuest = MyQuest.objects.get(slug=myQuest_name_slug)
    except MyQuest.DoesNotExist:
        myQuest = None

    if (current_user == avatar.user):
        context_dict = {'myQuest':myQuest, 'myQuest_title':myQuest.title, 'myQuest_description':myQuest.description, 'myQuest_req_professional_points':myQuest.req_professional_points, 'myQuest_req_athletic_points':myQuest.req_athletic_points, 'myQuest_req_academic_points':myQuest.req_academic_points}
        
        # Check if users avatar has cleared some of the required number of points to clear
        if (avatar.num_professional_points >= myQuest.req_professional_points):
            context_dict['myQuest_req_professional_points'] = "Clear!"
        if (avatar.num_athletic_points >= myQuest.req_athletic_points):
            context_dict['myQuest_req_athletic_points'] = "Clear!"
        if (avatar.num_academic_points >= myQuest.req_academic_points):
            context_dict['myQuest_req_academic_points'] = "Clear!"

        # if all three requirements are cleared the myQuest has been cleared
        if (context_dict['myQuest_req_academic_points'] == "Clear!" and context_dict['myQuest_req_athletic_points'] == "Clear!" and context_dict['myQuest_req_professional_points'] == "Clear!"):
            context_dict['myQuest_cleared'] = "Well Done!"
        return render(request, 'real_fantasy_adventure_app/myQuest.html', context_dict)
    else:
        return HttpResponseRedirect('/real_fantasy_adventure_app/')

@login_required(login_url='/real_fantasy_adventure_app/notLoggedIn/')
def add_myQuest(request, avatar_name_slug):
    """
    View handles the creation of myQuests by authenticated, active, and present avatars.
    Makes sure that myQuests can only be added if form is valied and saves it as part of
    the myquests connected to the avatar in question. Single field validation on site
    is performed in the template using bootstrap-django-forms
    """
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

def statChange(request, avatar_name_slug):
    """
    This view handles the logging in of hours made by users to their avatar, using functions
    from the statChange module. Checks if inputted number of hours is below 24 hours by
    redirecting to a punishment page for trying to cheat or put in invalid data
    """
    try:
        avatar = Avatar.objects.get(slug=avatar_name_slug)
    except:
        avatar = None

    if (request.method == 'POST'):
        form = StatChangeForm(request.POST)
        if form.is_valid():
            if avatar:
                formValues = form.cleaned_data
                # we can do the check here for 24 hours actually.
                inc_professional_points(avatar, formValues['num_professional_points'])
                inc_athletic_points(avatar, formValues['num_athletic_points'])
                inc_academic_points(avatar, formValues['num_academic_points'])
                return avatarProfile(request, avatar_name_slug)
            else:
                print form.errors
    else:
        form = StatChangeForm()
        context_dict = {'form': form, 'avatar': avatar, 'avatar_name_slug': avatar_name_slug}

    return render(request, 'real_fantasy_adventure_app/statChange.html', context_dict)


def rankings(request):
    """View collects the data needed from the database to present the rankings of users based on each of the categories"""
    avatars_by_academic = Avatar.objects.order_by('-num_academic_points')
    avatars_by_professional = Avatar.objects.order_by('-num_professional_points')
    avatars_by_athletic = Avatar.objects.order_by('-num_athletic_points')
    
    context_dict = {'professionals': avatars_by_professional, 'athletes': avatars_by_athletic, 'academics': avatars_by_academic}

    return render(request, 'real_fantasy_adventure_app/rankings.html', context_dict)

