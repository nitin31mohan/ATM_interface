# ATM interface using CSV file containg corresponding PINs, Names, and Balances

from tempfile import NamedTemporaryFile
import shutil
import csv

class ATM(object):

	def __init__(self, usr_pin):
		# takes user's input
		self.usr_pin = usr_pin

	def chooser(self, filename, tempfile, fields):
		self.filename = filename
		self.tempfile = tempfile
		self.fields = fields

		print("-------------ATM-------------")
		print("Enter choice for function...\n")
		print("""
			'1' => Deposit amount
			'2' => Withdrawal
			'3' => Account current status/Details
			'4' => Exit
			""")

		ch = int(input())

		if ch == 1:
			print("Enter amount to be deposited...\n")
			usr_bal = int(input())
			with open(filename, 'r') as csvfile, tempfile:
				reader = csv.DictReader(csvfile, fieldnames=fields)
				writer = csv.DictWriter(tempfile, fieldnames=fields)
				for row in reader:
					if row['pin'] == str(self.usr_pin):
						print('Making deposit...')
						temp = int(row['bal'])
						temp += usr_bal
						row['bal'] = str(temp)
						row = {'pin': row['pin'], 'accHolderName': row['accHolderName'], 'bal': row['bal']}
					writer.writerow(row)
			shutil.move(tempfile.name, filename)

		elif ch == 2:
			print("Enter amount to be withdrawn...\n")
			usr_bal = int(input())
			with open(filename, 'r') as csvfile, tempfile:
				reader = csv.DictReader(csvfile, fieldnames=fields)
				writer = csv.DictWriter(tempfile, fieldnames=fields)
				for row in reader:
					if row['pin'] == str(self.usr_pin):
						print('Making withdrawal...')
						temp1 = int(row['bal'])
						temp2 = temp1
						temp1 -= usr_bal
						if temp1 < 0:
							print("Balance below Rs. 0.00\nCannot sanction withdrawal\n")
							row['bal'] = str(temp2)
						else:
							row['bal'] = str(temp1)
					row = {'pin': row['pin'], 'accHolderName': row['accHolderName'], 'bal': row['bal']}
					writer.writerow(row)
			shutil.move(tempfile.name, filename)

		elif ch == 3:
			with open(filename, 'r') as csvfile, tempfile:
				reader = csv.DictReader(csvfile, fieldnames=fields)
				# writer = csv.DictWriter(tempfile, fieldnames=fields)
				for row in reader:
					if row['pin'] == str(self.usr_pin):
						print('Current balance is...')
						print("Rs. " + row['bal'] + " for the bank account of " + row['accHolderName'])
						temp = int(row['bal'])
						if temp < 0:
							print("Balance below Rs. 0.00")
							break

		elif ch == 4:
			print("Quiting...")
			exit()

		else:
			print("Incorrect input. Try again...")
			self.chooser(filename, tempfile, fields)

class ATM_Interface(ATM):
	print("Enter the PIN for your Account...\n")

	usr_pin = input()

	filename = './details.csv'
	tempfile = NamedTemporaryFile(mode='w', delete=False)

	fields = ['pin', 'accHolderName', 'bal']

	atm = ATM(usr_pin)
	atm.chooser(filename, tempfile, fields)
