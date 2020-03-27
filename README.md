# COVID19-Tracker
A python webapp using Django to visualize the recent outbreak of COVID-19. Sources for the data include JHU CSSE and BNO.
The live version can be found at [covid19app.live](http://covid19app.live)

## Screenshot:
![Screenshot of the main page featuring a table, a map and a chart highlighting confirmed cases and deaths](https://i.imgur.com/njZvR21.png)

## How to set up a local copy:
### Step 1: Clone the repository
### Step 2: Create a virtualenv
I'm assuming that you already have Python3 and pip installed on your system. If you don't have them you'll need to run    
```
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev
```
   
   
I'd recommend installing the dependencies in a virtualenv, but this is no necessity.   
If you do not want to set up a virtual environment, skip this step.   
       
First install virtualenv using pip:
```
$ sudo -H pip3 install --upgrade pip
$ sudo -H pip3 install virtualenv
```
After that you'll need to create a Python virtual environment (in the project directory):
```
$ virtualenv my-env
```
This will create a folder named "my-env" in your project directory.
Next activate the virtualenv with the following command.
```
$ source my-env/bin/activate
```
You will know you did everything right, when (my-env) appears in your prompt. It should look like this:
```
(my-env) user@host:~/covid19_tracker$
```

### Step 3: Installing dependencies
With your virtual environment active (or without it if you chose to skip the last step), you can now install the dependencies. I've added a requirements.txt to this repository, so installing all dependencies can be done with a single command.
```
$ pip install -r requirements.txt
```

This will install all dependencies listed in the requirements.txt into your environment. If it fails, make sure you're in the same directory as the requirements.txt.

### Step 4: Setting up the database
Before you can start using the app, you'll need to run a few commands for the database to work properly.    
You should still be in the directory where the requirements.txt resides, as youll need to run the manage.py file, which is also in that directory.
```
$ python manage.py makemigrations
$ python manage.py migrate
```

This will prepare the database for future use.

### Step 5: First run
You can now start the Django development server using `python manage.py runserver` . This will start the server on 127.0.0.1:8000.
Upon visiting the site for the first time, the script will initialize the database with data from the JHU CSSE's repository. This might take a few moments. This will not happen on subsequent runs, as long as you do not flush the database. The data displayed on the site is updated hourly from BNO's spreadsheet, the data for the graphs is updated daily from JHU CSSE's repository

### Step 6: Make improvements!
If you like what you see, but there are features missing, feel free to fork this repository and submit a pull request. Likewise if you notice a bug feel free to create an issue and I'll look into it as soon as possible
