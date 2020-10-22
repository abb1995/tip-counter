import time
import os

#		write module
#	everything pertaining to 
#	saving data to files can
#	be found in this module.
#	Any new functions that
#	require writing to file
#	should be placed here.

#Start data class.
class data(object):

	#Instantiation function.
	def __init__(self):
		pass

	#Function to write data to file.
	def writeToFile(self, orderNum, address, total, paid, date, road, store):
		#Takes given variables and calculates tip for that order.
		tip = float(paid) - float(total)
		#Keep track if the given order already exists in file.
		writeEntry = True
		#Opens file as 'a' to create the file if not already created.
		with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'a') as createFile:
			createFile.write('')
			#Opens as 'r+' to check if given order already exists in file.
			with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'r+') as f:
				#Checks every line and looks to see if order numbers match.
				for line in f.readlines():
					if (line[:6] == orderNum):
						writeEntry = False
						break
					else:
						writeEntry = True

			#Don't forget to close your files :)
			f.close()
			
			#If order does not already exist in file, this will write the order
			#in the following format:
			#123123 test address total:35.50 40.50 5.0
			if writeEntry == True:
				createFile.write(orderNum + ' ' + address + ' total:' + str(total) + ' ' + str(paid) + ' ' + str(tip)  + '\n')
			#If order already exists, will not write to file and will return error to user.
			elif writeEntry == False:
				print('Sorry that entry already exists.')

			#Writes time clock values to file if given.
			if road != 'null' and store != 'null':
				createFile.write('road: ' + road + '\n')
				createFile.write('store: ' + store + '\n')

		createFile.close()

	#Function used to import a complete file.
	def inputFile(self, path, date):
		#Keeps track if file exists or not.
		fileExists = False
		#Keeps track if user wants to overwite existing file.
		answer = 'y'
		#Looks in the \data\ directory to check if file for 
		#specified date already exists.
		for root, dirs, filenames in os.walk('.\\data\\'):
			for files in filenames:
				#If files is found, sets fileExists value to True and
				#prompts user if they would like to overwrite.
				if files == date + '.txt':
					answer = raw_input('File alread exists, overwrite it?(Y,N) ')
					fileExists = True
		#Trys to open designated file loaction to import data.
		try:
			#If file is existing and the user would like to overwrite it
			#this will remove the current file and start importing data.
			if fileExists == True and answer.lower() == 'y':
				os.remove('.\\data\\' + date + '.txt')
				#Reads from designated file and converts template.
				#The template for the import file can be found in
				#the README.txt in the home directory for the script.
				with open(path, 'r+') as readFile:
					with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'a') as writeFile:
						#Reads over every line and grabs necessary data.
						for line in readFile.readlines():
							#Checks splice of line to determine what the line contains.
							if line[:14] == 'time on road: ':
								road = line[13:]
								writeFile.write('road: ' + road)
							elif line[:15] == 'time in store: ':
								store = line[15:]
								writeFile.write('store: ' + store)
							else:
								#Grabs values for order number, street address, order total,
								#amount paid to driver, and amount tipped to driver.
								orderNum = line[line.find('order number: ') + 14:line.find(', address:')]
								address = line[line.find('address: ') + 9:line.find(', cost:')]
								cost = line[line.find('cost: ') + 6:line.find(', paid:')]
								paid = line[line.find('paid: ') + 6:].split()
								tip = float(paid[0]) - float(cost)
								#Writes everything to file in necessary format.
								writeFile.write(orderNum + ' ' + address + ' total:' + str(cost) + ' ' + str(paid[0]) + ' ' + str(tip) + '\n')
					#Close your files yo.
					writeFile.close()
				readFile.close()
			#If user answers 'n' to overwriting file, it will not be overwritten
			#and data will not be imported.
			elif fileExists == True and answer.lower() == 'n':
				print 'File was not overwritten.'

			#Writes data to file. See comments above, as it is the same code.
			if fileExists == False:
				with open(path, 'r+') as readFile:
					with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'a') as writeFile:
						for line in readFile.readlines():
							if line[:14] == 'time on road: ':
								road = line[13:]
								writeFile.write('road: ' + road)
							elif line[:15] == 'time in store: ':
								store = line[15:]
								writeFile.write('store: ' + store)
							else:
								orderNum = line[line.find('order number: ') + 14:line.find(', address:')]
								address = line[line.find('address: ') + 9:line.find(', cost:')]
								cost = line[line.find('cost: ') + 6:line.find(', paid:')]
								paid = line[line.find('paid: ') + 6:].split()
								tip = float(paid[0]) - float(cost)
								writeFile.write(orderNum + ' ' + address + ' total:' + str(cost) + ' ' + str(paid[0]) + ' ' + str(tip) + '\n')
					writeFile.close()
				readFile.close()
		#Returns error file could not be found at designated file location.
		except IOError:
			print('Could not find designated file.')