# python_sqlite_assignment
A python tool used to manage the Student table at the SQLite3 database, student.db

### Note: 
__2017/8/27 Updates:__
* __Refactored the tool using class.__
* __New schema: id, first_name, last_name, gender, class.__
* __Updated all methods to fit new schema.__
* __Added a schema method to print schema of table Student.__

__Initial commit:__
* __Implemented both long options and short options.__
* __Added an extra method, update.__
* __Students' first and last names should be only upper or lower letters, with hyphens between 1 and 10 characters.__

## Usage
* __python3 StudentDB.py -h, --help__

  Get help for different options.

* __python3 StudentDB.py -i, --init__

  Create a sqlite3 backend database called student.db with table Student. 
  
  If the database student.db exists, it would open it otherwise create a new one. If the table Student doesn't exist, if would create a new one otherwise drop it and then create a new one.

* __python3 StudentDB.py -a, --add <id> <first_name> <last_name> <gender> <class>__
  
  Add student to database table. 

* __python3 StudentDB.py -l, --list__
  
  List all students in the database.

* __python3 StudentDB.py -r, --remove <id>__
  
  Delete the student from the database. 

* __python3 StudentDB.py -u, --update <id> <first_name> <last_name> <gender> <class>__
  
  Update the student in the database to a new name. 
