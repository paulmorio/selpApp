# README #
## Software Large Engineering Practical Project for Paul Scherer (s1206798) ##
## UG3 2014-2015 ##

**Project Name:**: Real Fantasy Adventure

**Proposal Part 1**: Found under proposal.pdf or its source can be found under proposal.tex in the info folder

**Report Part 2**: Found under report.pdf or its source as report.tex in the info folder

**Note:** Its highly recommended to read the report first.

### Quick-Start ###
This section outlines how to quickly get correct environment, get the website started, populate the database, 
create an admin and run the unit tests written for this project.

#### Environment ####
It is highly recommended that the folder containing this readme be placed in another folder
which can be called anything (but for this example called 'selp') and then create an virtual
environment at this level with python 2.7.8 as the base called 'env'. On DICE this is

	virtualenv --python=/usr/bin/python2.7 env

After this is complete the following directory tree should result

	selp
	  |
	  |_selpApp
	  |
	  |_env

Inside of the 'selp' directory please run the following command to activate the environment

	source env/bin/activate

Checking that python from the virtualenv is used can be checked by running 'which python'.
Deactivating the virtualenv can be done by simply calling 'deactivate' but please do not do this
for not. 

Please install the required packages that are needed for this by running this command

	pip install -r requirements.txt

This command will install all of the packages list in the file requirements.txt from top to bottom.
If anything fails to install, please attempt installing again by running

	pip install <missing_package>

With this the environment should be ready.

#### Get the Web Application Running ####
##### Use Submitted Instance (Ready to go) #####
**Check next section if a completely new instance is desired** 

With the environment setup and activated, it is likely that I have submitted the project with
everything set-up, database populated, superuser admin created. In this case please cd into 
selpApp/rfa_website, ie.

	cd selpApp/rfa_website

And then start the django built in server

	python manage.py runserver

and point a browser to 

	http://localhost:8000/real_fantasy_adventure_app/

for the web app or

	http://localhost:8000/admin

for the admin page. In this case the username is 'admin' and password is 'test1234'

##### Start a new instance of project #####
If it is desired to start a completely fresh rfa-instance (rfa = Real Fantasy Adventure) 
with fresh database and admin, etc. please remove all of the migrations (please do not 
delete the folder) in this path (note this is not a command)

	selp/selpApp/rfa_website/real_fantasy_adventure_app/migrations

delete the database if present (once again not a command)

	selp/selpApp/rfa_website/db.sqlite3

After successfully completing these two steps, please create a new database, create
tables for the models, etc. from inside

	selp/selpApp/rfa_website/

directory with the commands:

	python manage.py && python manage.py makemigrations && python manage.py migrate

This should have created a new database with it notified of its models (if the second and third 
commands make sure of this).

###### Create Super User (aka admin) ######
Create a superuser with this command and fill in the relevant fields

	python manage.py createsuperuser

With this done it should actually be possible to access the website and the admin page already
via the commands shown in the first case. However its quite boring with no users, avatars, and 
so on. Thus we must populate the database with test users.

###### Populating the database ######
Inside the directory (where we should currently be)

	selp/selpApp/rfa_website

Please run the database population script

	python populate.py

This script will create 100 test Users, 100 Avatars, and 3 MyQuests for each avatar (totaling 
in 300). However if you would like to change this, the populate.py file has two global variables
just above the populate function that control the amount of users/avatars created and how many
MyQuests are created for each avatar. 

#### Testing ####
All of the unittests can be found in the file (not a command)

	selp/selpApp/rfa_website/real_fantasy_adventure_app/tests.py

This file consists of 75 unit tests, that tests various aspects of the web application. The 
django test suite can be run in the directory (not a command)

	selp/selpApp/rfa_website

with the command

	python manage.py test real_fantasy_adventure_app

coverage can be calculated via the coverage package and run with this command

	coverage run --source='.' manage.py test real_fantasy_adventure_app

the coverage report can be read with 

	coverage report

This concludes the quickstart guide. Once again the server can be run from

	selp/selpApp/rfa_website

with the commands 

	python manage.py runserver

and point a browser to 

	http://localhost:8000/real_fantasy_adventure_app/

for the web app or

	http://localhost:8000/admin

for the admin page.


### Questions to Self for Project Report ###
Hopefully yes to most questions.

#### General #### 
- Are the requirements fulfilled?
- Is your code maintainable? ie clean and reusable?
- Do you have appropiate documentation? In your code? Outside your code? Sphinx?
- Have you used source version control correctly?
- Have you tested your code? Do you have any automated tests?
- Does your porject work on DICE unmodified?
- Is your code production quality? Is it adaptable enough to be deployed?
- Have you spent the allocated amount of time on this project?
- Is your web application able to run on DICE and be accessible via a browser on DICE?
- LOL DOES IT WORK?

#### Project Specific ####
- Is there a notion of a user account?
- Are the users or a part of them ranked?
- What kind of ranking system did you use?
- How are the users re-ranked? Can it scale to large amount of users?
- How are you motivate moving up the ladder?
- You are relying on user honesty, are there any intentions on making this not so?
- Do you have a demo of it working, maybe via video?
- do you authenticate users (maybe via django)?
- Have you reported your failures and reason as to why this didnt work?

- The main three parts of the project: the readme, the git repository, and the report. Are they there?


#### Repository Specific ####

#### README specific ####
- Does it at least provide instruction for locally deploying and evaluating your website?
- Does it provide information on how to start the test suite and run this?
- Do ot describe the how to run the application inwords,demonstrate it with actual commands. Preferably this should consist of ONE COMMAND.
- Does the README give an indication on how to navigate the source code? Ie is the structure described (maybe just a pointer to the report if its described there?)? Where are the tests?

#### Report specific ####
- The report is intended to be relatively short.
- it is an opportunity to highlight things which you have done, even if it may not be apparent in the project. Write things you are especially things you are particularly proud of, and the things that are not perfect.
- It is a place to explain things if you had more time and resources as well.
- it is an opportunity to describe mistakes and difficulites you had.
	- for example you may have a poor design which will lose you marks, but acknowledging this poor design and commenting on it, why you did it in this way in the first place. etc will give you some marks.
- Simply recognising a shortcoming is at least demonstrating a critical apporach to your own work
- Producing an application with a poor design, structure or process, is unfortunate. failing to recognize that you have done so, is often disastrous. The report is the place to deomnstrate that you ahve recognised this.
- Justify your own design choices.

