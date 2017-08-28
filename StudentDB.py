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
		self.cursor.execute("CREATE TABLE Student (id varchar(5) PRIMARY KEY, first_name varchar(10) NOT NULL, last_name varchar(10) NOT NULL, gender varchar(1), class varchar(1))")
		self.conn.close()
		print("Initialized empty table Student in database {}.".format(db_name))

	# Add a student to database table
	def add(self, args):
		student_id, first_name, last_name, gender, class_name = args
		self.cursor.execute("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", [student_id, first_name, last_name, gender, class_name])
		self.conn.commit()
		self.conn.close()
		print("Student record", args, "added into table Student.")

	# List all students in the database
	def list(self):
		self.cursor.execute("SELECT * FROM Student")

		# Print table header BEGIN
		descriptions = self.cursor.description
		for description in descriptions:
			print("{:15s}".format(description[0]), end = '')
		print()
		for description in descriptions:
			print('-' * 15, end = '')
		print()
		# Print table header END

		for row in self.cursor.fetchall():
			for column in row:
				print("{:15s}".format(column), end = '')
			print()
		self.conn.close()

	# Delete the student from the database
	def remove(self, student_id):
		self.cursor.execute("SELECT * FROM Student WHERE id=?", [student_id])
		record = self.cursor.fetchone()
		if record is None:
			print("No matched record for student id " + student_id + ".")
		else:
			self.cursor.execute("DELETE FROM Student WHERE id=?", [student_id])
			self.conn.commit()
			print("Student record ", record, "removed from table Student.")
		self.conn.close()

	# Update the student in the database
	def update(self, args):
		student_id, first_name, last_name, gender, class_name = args
		self.cursor.execute("SELECT * FROM Student WHERE id=?", [student_id])
		number_of_records = len(self.cursor.fetchall())
		if number_of_records == 0:
			print("No matched records for student id \"" + student_id + "\".")
		else:
			self.cursor.execute("UPDATE Student SET first_name=?, last_name=?, gender=?, class=? WHERE id=?", [first_name, last_name, gender, class_name, student_id])
			self.conn.commit()
			print("Changed student id \"" + student_id + "\" to", args[1:] )
		self.conn.close()

	# Print the schema of Student table
	def schema(self):
		self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='Student'")
		print(self.cursor.fetchone()[0])
		self.conn.close()

# Custom type to check the student_id argument. It's a string that consists of 5 digits of numbers.
def student_id_type(s):
	s = s.strip()
	if re.match(r"^[0-9]{5}$", s):
		return s
	else:
		raise argparse.ArgumentTypeError("Student ID should be a 5-digit number.")

# Custom type to check the student name argument. It could include all letters both upper and lower cases with hyphens. Its length is between 1 and 10 characters inclusively.
def name_type(s):
	s = s.strip()
	if re.match(r"^[a-zA-Z-]{1,10}$", s):
		return s
	else:
		raise argparse.ArgumentTypeError("Student name should be only upper or lower cases letters, with hyphens between 1 and 10 characters.")

# Custom type to check the gender argument. It's either "M" for male or "F" for female.
def gender_type(s):
	s = s.strip()
	if re.match(r"^[MF]{1}$", s):
		return s
	else:
		raise argparse.ArgumentTypeError('Gender should be either "M" for male or "F" for female.')

# Custom type to check the class argument. It's one uppercase letter from A to Z.
def class_type(s):
	s = s.strip()
	if re.match(r"^[A-Z]{1}$", s):
		return s
	else:
		raise argparse.ArgumentTypeError("Class name should be a uppercase letter from A to Z.")

# Custom action to validate the arguments of the add method.
class ValidateInsertQuery(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		# print('%r %r %r' % (namespace, values, option_string))
		student_id, first_name, last_name, gender, class_name = values
		student_id_type(student_id)
		name_type(first_name)
		name_type(last_name)
		gender_type(gender)
		class_type(class_name)
		setattr(namespace, self.dest, values)

# ------------ argparse ------------
def main():

	parser = argparse.ArgumentParser(description="A python tool used to manage the Student table at the SQLite3 database, student.db")

	# Users could only use the following optional arguments one at a time. I also add short options along with the required long options.
	group = parser.add_mutually_exclusive_group()

	group.add_argument("-i", "--init", action="store_true", help="Create a sqlite3 backend database called student.db with table Student")

	group.add_argument("-a", "--add", nargs=5, action=ValidateInsertQuery, metavar=("id", "first_name", "last_name", "gender", "class"), help="Add student to database table")

	group.add_argument("-l", "--list", action="store_true", help="List all students in the database")

	group.add_argument("-r", "--remove", type=student_id_type, metavar="id", help="Delete the student from the database")

	group.add_argument("-u", "--update", nargs=5, action=ValidateInsertQuery, metavar=("id", "first_name", "last_name", "gender", "class"), help="Update the student in the database")

	group.add_argument("-s", "--schema", action="store_true", help="Show the schema of the Student table")

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
		dbManager.update(args.update)

	elif args.schema:
		dbManager = DBManager(db_name)
		dbManager.schema()

	else:
		print("Please select an option, use \"python3 StudentDB.py -h(-help)\" to see usage.")

if __name__ == '__main__':
	main()
