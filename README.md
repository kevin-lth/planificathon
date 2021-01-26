# Planificathon - Hackathon 2021

# Installation

## Clone the repository to your local machine

First, you will have to clone the repository. From now on, we will assume your current working directory is the cloned repository's directory.

Make sure you are on the main branch, otherwise you can change your branch with the following command:
```
git checkout main
```

Also check that you have Python 3 with a version above 3.6.

## Creation of virtual environments

### Windows 

To create a virtual environment for the project, run the following command:
```
python -m venv venv
```
Once installed, you can activate it as follows:
* Command Prompt
```
venv\Scripts\activate.bat
```
* PowerShell
```
venv\Scripts\Activate.ps1
```
You should see ```(venv)``` before the path.

In the virtual environment, install Django:
```
python -m pip install Django
```

To test if the installation went well, execute:
```
python test_installation\django_1.py
```
You should see a version number, such as ```3.1.5``` .

To run the app, use:
```
cd prototype
python manage.py runserver
```

To check if the server is working, open the URL shown in the console in a web browser.

When you are done, you can leave the virtual environment with the command:
```
deactivate
```

### Linux 

Before proceeding, make sure that virtual environments can be created on your system. You may need to install an additional package before being able to, such as ```python3-venv``` on Debian-based systems.

To create a virtual environment for the project, run the following command:
```
python3 -m venv venv
```
Once installed, you can activate it as follows:
```
source venv/bin/activate
```

In the virtual environment, install Django:
```
pip install django
```

To test if the installation went well, execute:
```
python test_installation/django_1.py
```
You should see a version number, such as ```3.1.5``` .

To run the app, use:
```
cd prototype
python manage.py runserver
```

To check if the server is working, open the URL shown in the console in a web browser.

When you are done, you can leave the virtual environment with the command:
```
deactivate
```
