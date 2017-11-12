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