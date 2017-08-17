#!/usr/bin/env python3

import argparse
import re
import sqlite3

db_name = "student.db"

def build():
	# Connection to SQLite3
	conn = sqlite3.connect(db_name)
	# Cursor
	return conn, conn.cursor()

# Initialization. Create a new Student table whether it exists or not.
def init():
	conn, c = build()
	c.execute("DROP TABLE IF EXISTS Student")
	c.execute("CREATE TABLE Student (Name varchar(30))")
	conn.close()
	print("Initialized empty table Student in database student.db.")

# Add a student to database table
def add(student_name):
	conn, c = build()
	c.execute("INSERT INTO Student VALUES (?)", [student_name])
	conn.commit()
	conn.close()
	print("Student named \"" + student_name + "\" added into table Student.")

# List all students in the database
def list():
	conn, c = build()
	c.execute("SELECT * FROM Student")
	column_names = [description[0] for description in c.description]
	print("{:30s}".format(column_names[0]))
	print("_" * 30)
	for row in c.fetchall():
		print("{:30s}".format(row[0]))
	conn.close()

# Delete the student from the database
def remove(student_name):
	conn, c = build()
	c.execute("SELECT * FROM Student WHERE name=?", [student_name])
	number_of_records = len(c.fetchall())
	if number_of_records == 0:
		print("No matched records for student named " + student_name + ".")
	else:
		c.execute("DELETE FROM Student WHERE name=?", [student_name])
		conn.commit()
		print(number_of_records, "record(s) of student(s) named \"" + student_name + "\" removed from table Student.")
	conn.close()
	

# Update the student in the database
def update(student_name_old, student_name_new):
	conn, c = build()
	c.execute("SELECT * FROM Student WHERE name=?", [student_name_old])
	number_of_records = len(c.fetchall())
	if number_of_records == 0:
		print("No matched records for student named \"" + student_name_old + "\".")
	else:
		c.execute("UPDATE Student SET name=? WHERE name=?", [student_name_new, student_name_old])
		conn.commit()
		print("Changed student(s) named \"" + student_name_old + "\" to " + student_name_new + ".", number_of_records, "record(s) changed.")
	conn.close()
	


# ------------ argparse ------------
def main():

	# Custom type to check the student name argument. It could include all letters both upper and lower cases with hyphen and(or) space in between the letters. Its length is between 1 and 30 characters inclusively.
	def name_type(s):
		s = s.strip()
		if re.match(r"^[a-zA-Z- ]{1,30}$", s):
			return s
		else:
			raise argparse.ArgumentTypeError("Student name should be only letters, with hyphen and space inside between 1 and 30 characters. Name should be quoted")

	parser = argparse.ArgumentParser(description="A python tool used to manage the Student table at the SQLite3 database, student.db")

	# Users could only use the following optional arguments one at a time. I also add short options along with the required long options.
	group = parser.add_mutually_exclusive_group()

	group.add_argument("-i", "--init", action="store_true", help="Create a sqlite3 backend database called student.db with table Student")

	group.add_argument("-a", "--add", type=name_type, help="Add student to database table")

	group.add_argument("-l", "--list", action="store_true", help="List all students in the database")

	group.add_argument("-r", "--remove", type=name_type, help="Delete the student from the database")

	group.add_argument("-u", "--update", type=name_type, nargs=2, help="Update the student in the database to a new name, use \"python3 StudentDB.py -u <student_name> <new_student_name>\"")

	args = parser.parse_args()
	if args.init:
		init()
	elif args.add:
		add(args.add)
	elif args.list:
		list()
	elif args.remove:
		remove(args.remove)
	elif args.update:
		update(args.update[0], args.update[1])
	else:
		print("Please select an option, use \"python3 StudentDB.py -h(-help)\" to see usage.")

if __name__ == '__main__':
	main()
