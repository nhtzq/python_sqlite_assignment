# python_sqlite_assignment
A python tool used to manage the Student table at the SQLite3 database, student.db

### Note: 
* __Implemented both long options and short options.__
* __Added an extra method, update.__
* __Student name should be only letters, with hyphen and space inside between 1 and 30 characters. Names are suggested to be quoted especially when there's space between first name and last name.__

## Usage
* __python3 StudentDB.py -h, --help__

  Get help for different options.

* __python3 StudentDB.py -i, --init__

  Create a sqlite3 backend database called student.db with table Student. 
  
  If the database student.db exists, it would open it otherwise create a new one. If the table Student doesn't exist, if would create a new one otherwise drop it and then create a new one.

* __python3 StudentDB.py -a, --add <student name>__
  
  Add student to database table. 

* __python3 StudentDB.py -l, --list__
  
  List all students in the database.

* __python3 StudentDB.py -r, --remove <student name>__
  
  Delete the student from the database. 

* __python3 StudentDB.py -u, --update <student name> <new_student name>__
  
  Update the student in the database to a new name. 
