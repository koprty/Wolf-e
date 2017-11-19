# Wolf-e


## Installation steps
#### Installing Dependencies
- Install Python
- Install Django, MySQL, MySQLClient
  - Django
    - You can use Anaconda for that
  - Mysql
  - MySql Client
    - `pip install mysqlclient`
  - Look at this [tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) to see how to run the project
  - `python manage.py runserver`
#### Setting up the Database
- Two options (create the database from Scratch
  - Create the MySQL Database
    - `mysql -u root -p < init_mysql.sql`
  - Import Database
    - TBD
- Database login:
  - user: lal
  - password: ALLCSE305<3
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
  - Under 'Shop', there is a 'ShopItems' row
  - Click '+Add'

## Applications
#### Shop
- Represents the interface for a customer to shop for items to add to the cart
##### Models
- ShopItem