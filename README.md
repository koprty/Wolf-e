# Wolf-e


## Installation steps
#### Installing Dependencies
- Install Python
- Install Django, MySQL, MySQLClient
  - Django
    - You can use Anaconda for that
    - `pip install django`
  - Mysql
    - Linux
        - `sudo apt-get install mysql-server`
  - MySql Client
    - `pip install mysqlclient`
  - Look at this [tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) to see how to run the project
  - `python manage.py runserver`

#### Setting up the Database
- Two options (create the database from Scratch
  - Create the MySQL Database
    - `mysql -u root -p < init_mysql.sql`
    - OR `sudo mysql < init_mysql.sql`
  - Import Database
    - TBD
- Database login:
  - user: lal
  - password: ALLCSE305<3
- Create a django superuser
  - python manage.py createsuperuser
  - (Note that you have to use a good password for this)
#### Resetting the Database
- Messed up or did the setting up not work?
  - Delete database and default mysql user:
    - `mysql -u root -p < reset_mysql.sql`
    - OR `sudo mysql < reset_mysql.sql`
#### Important useful comments for our project we used ;) 
- Convert database in MySQL to django models
  - `python manage.py inspectdb`
#### Admin page
- Accessing the Admin Page
  - Create a super user
    - `python manage.py createsuperuser`
  - Visit http://127.0.0.1:8000/admin/
- Adding an Item
  - Visit http://127.0.0.1:8000/admin/
  - Login

## Applications
#### Shop
- Represents the interface for a customer to shop for items to add to the cart
##### Models
- Item
- Review
    - New Key: ReviewId
    - Django does not support composite keys
    - A rating can be an int from 0 to 5
- Customer
##### Sessions
- We keep track of a customer's login session
  - Dev Notes, you can find if a customer has been logged in by calling the loggedin() function <- right now returns a boolean if loggedin or not
    - OR you can manually check the sessions attribute of each request
    - TODO: make login and register inaccessible if already loggedin

## Todos
- Add a Customer and their Accounts (in progress) 
- Add a seller
- Add an Employee who can login
- Add Transactions
- Add Delivery and Payments
- Calculate Rating/NumRatings for every Item
- Add Ratings form on Item Page
