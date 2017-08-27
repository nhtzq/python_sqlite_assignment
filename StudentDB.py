#!/usr/bin/env python3

import argparse
import re
import sqlite3

db_name = "student.db"

class DBManager:
	def __init__(self, db_name):
		# Connection to SQLite3
		self.conn = sqlite3.connect(db_name)
		# Cursor
		self.cursor = self.conn.cursor()

	# Initialization. Create a new Student table whether it exists or not.
	def init(self):
		self.cursor.execute("DROP TABLE IF EXISTS Student")
		self.cursor.execute("CREATE TABLE Student (Name varchar(30))")
		self.conn.close()
		print("Initialized empty table Student in database {}.".format(db_name))

	# Add a student to database table
	def add(self, student_name):
		self.cursor.execute("INSERT INTO Student VALUES (?)", [student_name])
		self.conn.commit()
		self.conn.close()
		print("Student named \"" + student_name + "\" added into table Student.")

	# List all students in the database
	def list(self):
		self.cursor.execute("SELECT * FROM Student")

		# Print table header BEGIN
		descriptions = self.cursor.description
		for description in descriptions:
			print("{:30s}".format(description[0]), end = '')
		print()
		for description in descriptions:
			print('-' * 30, end = '')
		print()
		# Print table header END

		for row in self.cursor.fetchall():
			for column in row:
				print("{:30s}".format(column), end = '')
			print()
		self.conn.close()

	# Delete the student from the database
	def remove(self, student_name):
		self.cursor.execute("SELECT * FROM Student WHERE name=?", [student_name])
		number_of_records = len(self.cursor.fetchall())
		if number_of_records == 0:
			print("No matched records for student named " + student_name + ".")
		else:
			self.cursor.execute("DELETE FROM Student WHERE name=?", [student_name])
			self.conn.commit()
			print(number_of_records, "record(s) of student(s) named \"" + student_name + "\" removed from table Student.")
		self.conn.close()

	# Update the student in the database
	def update(self, student_name_old, student_name_new):
		self.cursor.execute("SELECT * FROM Student WHERE name=?", [student_name_old])
		number_of_records = len(self.cursor.fetchall())
		if number_of_records == 0:
			print("No matched records for student named \"" + student_name_old + "\".")
		else:
			self.cursor.execute("UPDATE Student SET name=? WHERE name=?", [student_name_new, student_name_old])
			self.conn.commit()
			print("Changed student(s) named \"" + student_name_old + "\" to " + student_name_new + ".", number_of_records, "record(s) changed.")
		self.conn.close()

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
		dbManager = DBManager(db_name)
		dbManager.init()

	elif args.add:
		dbManager = DBManager(db_name)
		dbManager.add(args.add)

	elif args.list:
		dbManager = DBManager(db_name)
		dbManager.list()

	elif args.remove:
		dbManager = DBManager(db_name)
		dbManager.remove(args.remove)

	elif args.update:
		dbManager = DBManager(db_name)
		dbManager.update(args.update[0], args.update[1])

	else:
		print("Please select an option, use \"python3 StudentDB.py -h(-help)\" to see usage.")

if __name__ == '__main__':
	main()
