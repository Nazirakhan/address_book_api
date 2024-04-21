1. Install python version 3.11.6 from python.org
  link: to download python "https://www.python.org/downloads/release/python-3116/"
  install according to OS windows/MacOS/linux

clone the repository or you can download the repository

  As i have provided all those files in this repository one doesn't need to install any of this just install the python itself.

 open powershell inside the project folder.
 activate the virtual environment by using command "virtualenv/Scripts/activate"
 after activating the virtual environment run command "python manage.py runserver" to start the django server.

 open any browser and type "http://127.0.0.1:8000/api/docs/" to open the link in browser.

 to create a new user user open this "/api/user/create/" and add your user details by clicking on try it out button.
 after this response should be 201 created.

then got to /api/user/token/ to generate token number for validation by providing your user credential by clicking on try it out. which will generate a token number in response body.

copy the token values only and scroll up to the top and click on Authorize button to open and scroll down to tokenAuth (apiKey) form field and provide the value like this:
Token 54cxxxxxxxxxxxx
then click authorize. to get authorize and start using those api url.

  Below mention instruction and commands for reference purpose to create those project setup.

create virtual environment provided by python itself.
command : python -m venv <virtual_environment_name>
e.g: python -m venv virtualenvi

to activate virtual environment open the powershell terminal in the location where virtual environment was created and run command.
command: <virtual_environment_name>/Scripts/activate
e.g: virtualenvi/Scripts/activate

if using linux or git bash:
command: source <virtual_environment_name>/Scripts/activate

update pip using command:
 python.exe -m pip install --upgrade pip

install all the dependencies from requirements.txt file
command- pip install -r requirements.txt

create django project by running command.
command: django-admin startproject projectname

navigate to the projectname folder and look for manage.py file
the in powershell to run django server run the following command.
command: python manage.py runserver
which will run the django server on 127.0.0.1:8000 link.

