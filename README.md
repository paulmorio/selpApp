# README #
## Software Large Engineering Practical Project ##
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
environment at this level with python 2.7.8 as the base called 'env'.

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




