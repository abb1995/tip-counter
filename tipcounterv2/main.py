#Import necessary modules.
import time
import os
import write
import read

#Startup
print '                                         '
print '-----------------------------------------' 
print '     Tip Counter made by Austin Bevil    '
print '-----------------------------------------'
print '     Please read the readme located in   '
print '     the programs main folder before     '
print '     using this. It contains crucial     '
print '     information regarding all the       '
print '     commands and what they do.          '
print '-----------------------------------------'
print '     Tip Counter made by Austin Bevil    '
print '-----------------------------------------'
print ' '

#Used to check if clock times are already in file
checkRoad = True
checkStore = True

#instantiation
save = write.data()
search = read.data()

userInput = raw_input('Please enter the action you would like to perform. ')

if userInput.lower() == 'save':
	#keeps track of how many orders have been entered.
	i = 1
	orderAmount = raw_input('How many orders do you have to store? ')
	#Takes input on how many order you need to store, and will
	#continue to take input for each order until limit has been reached.
	while i <= int(orderAmount):
		i += 1
		#Takes input for order number, street address, order price, 
		#amount paid to driver, and the date to save the data to.
		orderNum = raw_input('Please enter the 6-digit order number: ')
		address = raw_input('Please enter the address delivered to: ')
		total = raw_input('Please enter the total on the order: ')
		paid = raw_input('Please enter the amount paid to you: ')
		date = raw_input('Please enter the date you would like to save this information for(leave blank for today\'s date): ')
		#Enters the current days date if date is left empty by user.
		if date == '':
			date = time.strftime('%m-%d-%y')

		#Trying to a non-existant files with 'r+'' will throw IOError,
		#this opens the files with 'a' to create the file if it does not exist.
		with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'a') as f:
			f.write('')
		f.close()

		#Opens the requested date's file to check if clock times are already entered.
		with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'r+') as checkFile:
			for line in checkFile.readlines():
				if line[:5] == 'road:':
					checkRoad = False
				if line[:6] == 'store:':
					checkStore = False
		checkFile.close()

		#If clocktimes are not present in requested date's file, will request
		#input for clock times on that day.
		if checkRoad == True and checkStore == True:
			onRoad = raw_input('Please enter your time on the road for this date: ')
			inStore = raw_input('Please enter your time in the store for this date: ')
		else:
			onRoad = 'null'
			inStore = 'null'
		print ' '
		#Runs function with all relavant data.
		save.writeToFile(orderNum, address, total, paid, date, onRoad, inStore)

if userInput.lower() == 'search':
	#Asks for input on how to search. By specific date, or entire directory.
	#If searching entire directory, script will return all entries for 
	#that order number and ask to choose which one the user would like to view.
	answer = raw_input('How would you like to search?(date, directory) ')
	#If user would like to search by specific date, this gets the date and order number
	#and runs the get_data function.
	if answer == 'date':
		date = raw_input('Please enter the date you would like to search. \n')
		orderNum = raw_input('Please enter the order number you would like to search for. \n')
		print ' '
		search.returnData(date, orderNum)
	#If user would like to search through entire directory, script only takes 
	#input on order number and runs get_data function.
	elif answer == 'directory':
		orderNum = raw_input('Please enter the full 6-digit order number to search for. \n')
		print ' '
		search.returnData('all', orderNum)
	#Will return error if no valid command is entered.
	else:
		print 'Sorry, that is an invalid command.'

if userInput.lower() == 'total':
	#Takes input for the date the user would like totals for and
	#runs the get_total function.
	date = raw_input('Please enter the date you would like totals for. \n')
	print ' '
	search.returnTotal(date)

#Run input_file function.
if userInput.lower() == 'import':
	#Takes input for the path of the file to import, and the date
	#to import the data to and runs the input_file function.
	path = raw_input('Please enter the file path: ')
	date = raw_input('Please enter the date to attatch this file to: ')
	print ' '
	save.inputFile(path, date)

if userInput.lower() == 'range':
	startDate = raw_input('Please enter the starting date: ')
	endDate = raw_input('Please enter the ending date: ')
	print ' '
	search.returnRange(startDate, endDate)

#Waits for user to press enter so that command window does not close
#after script has complete.
raw_input('Press enter to continue...')
