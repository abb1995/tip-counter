import os
import time

#		read module
#	everything pertaining to 
#	reading data from files can
#	be found in this module.
#	Any new functions that
#	require reading from file
#	should be placed here.

#Start data class
class data(object):

	#Instantiation function.
	def __init__(self):
		pass

	#Function to return data from specific date
	#or for a specified order number in all dates.
	def returnData(self, date, orderNum):
		#Keeps track of the number of orders found.
		increment = 1
		#Puts dates the orders were found into list.
		ordersFound = []
		#Kepps track if order exists.
		fileFound = False
		#If user searches by directory.
		if date == 'all':
			#Looks through every file in the \data directory.
			for root, dirs, filenames in os.walk('.\\data'):
				for f in filenames:
					#Opens file to look for order number.
					with open(os.path.realpath('.') + '\\data\\' + f, 'r') as checkFile:
						for line in checkFile.readlines():
							#If order number is found, add date order number
							#was found in to list.
							if line[:6] == orderNum:
								ordersFound.append(f)
								fileFound = True
					checkFile.close()

			#Return error if order is not found in any files.
			if fileFound == False:
				print 'Sorry, I was unable to locate the requested order in my records.'
			#Lists the dates order was found in.
			else:
				print 'The order you searched for was found in the following dates: '

				#Prints out each date in the list with a number listed next to it
				#and asks user which date they would like to view by entering 
				#the respective number.
				for i in ordersFound:
					print str(increment) + ': ' + i
					increment += 1

				answer = raw_input('Which file would you like to view? ')
				print ' '

				#Opens the file attached to the number the user entered to grab requested data.
				with open(os.path.realpath('.') + '\\data\\' + ordersFound[int(answer) - 1]) as returnStats:
					for lines in returnStats.readlines():
						#Finds the order in the file and returns all relevant data.
						if lines[:6] == orderNum:
							address = lines[7:lines.rfind('total')]
							moneyList = lines[lines.rfind('total') + 6:].split()
							print 'Order number ' + orderNum
							print 'Address: ' + address
							print 'Order Total: $' + moneyList[0]
							print 'Amount Paid: $' + moneyList[1]
							print 'Total Tip: $' + moneyList[2]
				returnStats.close()

		#If user searches by specific date.
		else:
			#Tries to open the file requested.
			try:
				with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'r+') as f:
					for line in f.readlines():
						#If order is found, return relevant data.
						if line[:6] == orderNum:
							address = line[7:line.rfind('total')]
							moneyList = line[line.rfind('total') + 6:].split()
							print 'Order number ' + orderNum 
							print 'Address: ' + address
							print 'Order Total: $' + moneyList[0]
							print 'Amount Paid: $' + moneyList[1]
							print 'Total Tip: $' + moneyList[2]
							fileFound = True
				f.close()

				#If order is not found, return error to user.
				if fileFound == False:
					print 'Sorry, I could not find the requested order for that day.'

			except EnvironmentError:
				print 'File was not found'

	#Function to return totals for a specified date.
	def returnTotal(self, date):
		numberOfOrders = 0
		#Per hour pay while on the road. Should always be 5.00
		roadPay = 5.00
		#Per hour pay while in the store, this is dependant on what your position is.
		storePay = 9.00
		#Mileage paid out per delivery. This value fluctuates.
		mileage = 1.25
		#Hours on road and in store.
		timeOnRoad = 0
		timeInStore = 0
		#Keeps track if file exists.
		fileExists = False
		#Keeps track of total amount of tips.
		tipTotal = 0
		#Keeps track of the total cost of all orders combined.
		storeTotal = 0
		for root, dirs, filenames in os.walk('.\\data'):
			for files in filenames:
				#Looks through directory to find requested date.
				if files == date + '.txt':
					fileExists = True
					#Opens file to gather necessary data.
					with open(os.path.realpath('.') + '\\data\\' + date + '.txt', 'r+') as readFile:
						for line in readFile.readlines():
							#If line contains time clock times, grab values.
							if line[:5] == 'road:':
								timeOnRoad = float(line[5:])
							elif line[:6] == 'store:':
								timeInStore = float(line[6:])
							#Grab data from line for order.
							else:
								#Number of orders taken that day.
								numberOfOrders += 1
								orderNum = line[:7]
								address = line[7:line.rfind('total')]
								#Splits the last three values into a list.
								#[order total, amount paid, tip]
								moneyList = line[line.rfind('total') + 6:].split()
								#Adds up total amount of tips.
								tipTotal = tipTotal + float(moneyList[2])
								#Adds up order totals.
								storeTotal = storeTotal + float(moneyList[0])

						#Adds time clocks together to get total hours worked.
						totalWorkHours = timeInStore + timeOnRoad
						#Multiplies orders taken by mileage to get total amount of 
						#mileage paid out.
						totalMileage = numberOfOrders * 1.25
						#Divides total tips by orders taken to get average tip per delivery.
						avgTipPerRun = float(tipTotal) / numberOfOrders
						#Divides orders taken by total hours worked to get average delivery per hour.
						avgRunPerHour = numberOfOrders / totalWorkHours
						#Formula to calculate approximate hourly wage. This is based on your
						#average tips per run, average delivery per hour, and multiple other factors.
						approxHrWage = (((avgTipPerRun * avgRunPerHour) + (mileage * avgRunPerHour)) + ((roadPay * timeOnRoad) + (storePay * timeInStore)) / totalWorkHours)

						#Print out relevant data.
						print 'Total tips $%0.2f' % tipTotal
						print 'Total mileage $%0.2f' % totalMileage
						print 'Total tips plus mileage: $%0.2f' % (tipTotal + totalMileage)
						print 'Total amount pulled for store: $%.02f' % storeTotal
						print 'Total number of orders: ' + str(numberOfOrders)
						print 'Total hours worked: %.02f' % totalWorkHours
						print 'Average tip per run: $%0.2f' % avgTipPerRun
						print 'Average run per hour: %0.2f' % avgRunPerHour
						print 'Approximate Hourly Wage: $%0.2f' % approxHrWage
						print 'Time on road: %0.2f hours' % timeOnRoad
						print 'Time in store %0.2f hours' % timeInStore
						print 'Total time worked: %0.2f hours\n' % totalWorkHours
						break

				else:
					fileExists = False	
		#Returns error to user if file could not be found.
		if fileExists == False:
			print 'Sorry, I could not find the requested date in my records.'

	def returnRange(self, startDate, endDate):
		#splits the numbers separatley into a list
		startSplit = startDate.split('-')
		endSplit = endDate.split('-')
		#Keeps track of leap year.
		leap = False
		#Keeps track of the current date
		currentMonth = startSplit[0]
		currentDay = startSplit[1]
		currentYear = startSplit[2]
		currentDate = startDate
		#Keeps track of overall numbers
		days = 0
		overallTips = 0
		overallMileage = 0
		overallRuns = 0
		overallWorkHours = 0
		overallInStore = 0
		overallOnRoad = 0
		overallStoreTotal = 0
		numberOfOrders = 0
		#Per hour pay while on the road. Should always be 5.00
		roadPay = 5.00
		#Per hour pay while in the store, this is dependant on what your position is.
		storePay = 9.00
		#Mileage paid out per delivery. This value fluctuates.
		mileage = 1.25
		#Hours on road and in store.
		timeOnRoad = 0
		timeInStore = 0
		#Keeps track if file exists.
		fileExists = False
		#Reference for how many days are in each month.
		daysInMonth = {'01': 31, 
						'02': 28,
						'03': 31,
						'04': 30,
						'05': 31,
						'06': 30,
						'07': 31,
						'08': 31,
						'09': 30,
						'10': 31,
						'11': 30,
						'12': 31}

		#Loops through every day and tries to open the file for that day.
		while True:
			try:
				with open(os.path.realpath('.') + '\\data\\' + currentMonth + '-' + str(currentDay) + '-' + currentYear + '.txt', 'r+') as readFile:
					days += 1
					#Keeps track of total amount of tips.
					tipTotal = 0
					#Keeps track of the total cost of all orders combined.
					storeTotal = 0
					numberOfOrders = 0
					for line in readFile.readlines():
						#If line contains time clock times, grab values.
						if line[:5] == 'road:':
							timeOnRoad = float(line[5:])
						elif line[:6] == 'store:':
							timeInStore = float(line[6:])
						#Grab data from line for order.
						else:
							#Number of orders taken that day.
							numberOfOrders += 1
							#Splits the last three values into a list.
							#[order total, amount paid, tip]
							moneyList = line[line.rfind('total') + 6:].split()
							#Adds up total amount of tips.
							tipTotal = tipTotal + float(moneyList[2])
							#Adds up order totals.
							storeTotal = storeTotal + float(moneyList[0])

					#Adds time clocks together to get total hours worked.
					totalWorkHours = timeInStore + timeOnRoad
					#Keeps track of the overall numbers.
					overallWorkHours += totalWorkHours
					overallTips += tipTotal
					overallMileage += 1.25 * numberOfOrders
					overallRuns += numberOfOrders
					overallOnRoad += timeOnRoad
					overallInStore += timeInStore
					overallStoreTotal += storeTotal
				readFile.close()


			except IOError or EnvironmentError:
				pass

			#One the current date is equal to the end date, break out of the loop and return relevant data.
			if currentMonth + '-' + str(currentDay) + '-' + currentYear == endDate:
				#make final calculations
				averageTimeInStore = overallInStore / days
				averageTimeOnRoad = overallOnRoad / days
				averageHoursPerDay = overallWorkHours / days
				averageTipsPerDay = overallTips / days
				averageMileagePerDay = overallMileage / days
				averageDeliveriesPerDay = overallRuns / days
				averageStoreTotal = overallStoreTotal / days
				averageHourly = ((((averageTipsPerDay + averageDeliveriesPerDay) / averageHoursPerDay) + ((roadPay * averageTimeOnRoad) + (storePay * averageTimeInStore)) / averageHoursPerDay))
				print 'Your average time spent in the store:   %0.2f' % averageTimeInStore
				print 'Your average time spent on the road:    %0.2f' % averageTimeOnRoad
				print 'Your average hours worked per day:      %0.2f' % averageHoursPerDay
				print 'Your average deliveries taken per day:  ' + str(averageDeliveriesPerDay)
				print 'Your average tips per day:             $%0.2f' % averageTipsPerDay
				print 'Your average mileage paid out per day: $%0.2f' % averageMileagePerDay
				print 'Average cost of orders taken per day:  $%0.2f' % averageStoreTotal
				print 'Your average hourly rate:              $%0.2f' % averageHourly
				break

			#Check leap
			if (2000 + int(currentYear)) % 4 == 0:
				leap = True

			#Sets the format for the day. e.g. if the day is only 1 digit
			#add a 0 to the front, otherwise just add 1 to the day.
			if int(currentDay) + 1 < 10:
				currentDay = '0' + str(int(currentDay) + 1)
			else:
				currentDay = int(currentDay) + 1


			# if currentMonth == '02' and leap == True:
			# 	if (daysInMonth[currentMonth] + 1) < int(currentDay):
			# 		if (int(currentMonth) + 1) < 10:
			# 			currentMonth = int(currentMonth) + 1
			# 			currentMonth = '0' + str(currentMonth)
			# 		else:
			# 			currentMonth = str(int(currentMonth) + 1)

			#If the current month is not december, this will check if the current day
			#is higher than the amount of days in that month. If it is, it will
			#add 1 to the month and set the day to 01.
			if currentMonth != '12':
				#Grabs the amount of days in the current month, and checks if
				#the value for the current day is greater than that number.
				if daysInMonth[currentMonth] < int(currentDay):
					#Sets the format. e.g. if the value is only 1 digit
					#add a 0 to the front, otherwise just add 1 to the value.
					if (int(currentMonth) + 1) < 10:
						currentMonth = int(currentMonth) + 1
						currentMonth = '0' + str(currentMonth)
						currentDay = '01'
					else:
						currentMonth = str(int(currentMonth) + 1)
						currentDay = '01'

			#If the current month is december, this will check if the current day
			#is higher than the amount of days in december. If it is, it will
			#add 1 to the year and set the month and day to 01.
			if currentMonth == '12':
				#Grabs the amount of days in the current month, and checks if
				#the value for the current day is greater than that number.
				if daysInMonth[currentMonth] < int(currentDay):
					#Sets the format. e.g. if the value is only 1 digit
					#add 0 to the front, otherwise just add 1 to value.
					if (int(currentYear) + 1) < 10:
						currentYear = int(currentYear) + 1
						currentYear = '0' + str(currentYear)
						currentDay = '01'
						currentMonth = '01'
					else:
						currentYear = str(int(currentYear) + 1)
						currentDay = '01'
						currentMonth = '01'