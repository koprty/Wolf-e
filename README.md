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
- remove the shopping cart row in SQL created when you log in (no need for it, just display an empty shopping cart [logged in] or error [logged out]) - done (arjun?)
- customer object / item object for customerid / itemid?

- Shopping Cart Profile
    - Edit quantity

- Added Delivery and Payments form - lise (need to do more checks for cookies) 
- Create a detailed confirm order page w/ shopping cart - lise

- Add order history page

## Optional ToDos
- Customer Profile
- data stats maybe if we have time in this hacky project
- Revamp adminstration pages
- add images urls
- Add item description
- Notification bubbles when a form is submitted
- Add shopping cart icon to navbar

## Todones
- Login Page with Cookies
- Register Page
- Items
- Reviews with login 
- Login makes shopping cart
- Make sure you can't login twice
- update item quantities upon enacting a transaction
- Check for duplicate items in shopping cart
- Checkout flow -> Transaction

