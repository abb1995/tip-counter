#import required libraries and declare global variables.
import os
import time
lineNum = 0
start = ''
end = ''

#declare main function to re-run script when needed.
def main():
	global start
	global end
	#declare the function that stores the information obtained from the user into a file.
	def store(orderNum='', address='', total='', paid='', road='', Store='', date=time.strftime('%m-%d-%y'), clockTime=''):
		clocktime = False
		r = False
		s = False
		#converts the total amount and the amount paid to floats, then subtracts them to get the tip.
		tip = float(paid) - float(total)
		#tries to make an order directory. if it already exists, does nothing.
		try:
			os.mkdir('orders')
		except FileExistsError:
			pass
		#opens file for writing. if it doesnt exists, it creates it.
		with open(os.path.realpath('.') + '\\orders\\' + date + '.txt', 'a', encoding = 'UTF-8') as f:
			with open(os.path.realpath('.') + '\\orders\\' + date + '.txt', 'r+', encoding = 'UTF-8') as g:
				for line in g.readlines():
					if line[:5] == ('time:'):
						clocktime = True
					if line[:5] == 'road:':
						r = True
					if line[:6] == 'store:':
						s = True
			g.close()
			if clocktime == False:
				f.write('time: ' + clockTime)
			if r == False:
				f.write('road: ' + road)
			if s == False:
				f.write('store: ' + Store)
			f.close()
		with open(os.path.realpath('.') + '\\orders\\' + date + '.txt', 'a', encoding = 'UTF-8') as h:		
			h.write(orderNum + ' ' + address + ' total:' + str(total) + ' ' + str(paid) + ' ' + str(tip)  + '\n')

	def inputFile(loc, date):
		clocktime = ''
		orderNum = ''
		address = ''
		total = ''
		paid = ''
		road = ''
		Store = ''
		try:
			with open(loc, 'r', encoding = 'UTF-8') as f:
				for line in f.readlines():
					if line[:5] == 'time:':
						clocktime = line[5:]
					elif line[:5] == 'road:':
						road = line[5:]
					elif line[:6] == 'store:':
						Store = line[6:]
					else:
						orderNum = line[:3]
						address = line[4:line.rfind('total') - 1]
						stuff = line[line.rfind('total') + 6:].split()
						total = stuff[0]
						paid = stuff[1]
						store(orderNum, address, total, paid, road, Store, date, clocktime)
			f.close()
		except FileNotFoundError:
			print('Could not find file, please correct any mispellings and try again...')
		main()

	#declare the function that searches existing files and returns respective data.
	def search(date, num):
		#declares global variable to allow editing of it.
		global lineNum
		lineNum = 0
		OrderAddress = ''
		stuff = []
		OrderTotal = ''
		OrderPaid = ''
		OrderTip = ''
		#itterates through the orders directory.
		for root, dirs, filenames in os.walk('.\\orders'):
			for f in filenames:
				#looks for the specified file.
				if f == (date + '.txt'):
					with open(os.path.realpath('.') + '\\orders\\' + date + '.txt', 'r', encoding = 'UTF-8') as d:
						#itterates through every line of the file
						OrderNumber = ''
						for line in d.readlines():
							#keeps track of number of orders.
							lineNum += 1
							#seperates the order number from the rest of the line.
							if line[:3] == num:
								numExists = True
								OrderNumber = line[:3]
								#seperates address from the rest of the line.
								OrderAddress = line[4:line.rfind('total')]
								#stores everything after the address into a list.
								stuff = line[line.rfind('total') + 6:].split()
								OrderTotal = stuff[0]
								OrderPaid = stuff[1]
								OrderTip = stuff[2]
								OrderTip = float(OrderTip)
								#prints out requested data.
								print('Order Number: ' + OrderNumber)
								print('Order Address: ' + OrderAddress)
								print('Order Total: ' + OrderTotal)
								print('Order Paid: ' + OrderPaid)
								print('Order Tip: %0.2f' % (OrderTip))
								print()
								break
							else:
								numExists = False
		if numExists == False:
			print('Could not find specified order number...\n')
		main()

	#declare function to return total tips, mileage, and number of orders of a specific date.
	def total(date):
		#declares global variable to allow editing of it.
		global lineNum
		fileExists = False
		lineNum = 0
		tipTotal = 0.00
		timeOnRoad = 0
		tStart = ''
		tEnd = ''
		tTotal = 0
		clocktime = []
		stuff = []
		approxHrWage = 0
		timeOnRoad = 0
		avgRunPerHr = 0
		avgTipPerRun = 0
		road = ''
		Store = ''
		OrderTotal = 0
		#itterates through orders directory.
		for root, dirs, filenames in os.walk('.\\orders'):
			for f in filenames:
				#looks for the specified file.
				if f == (date + '.txt'):
					fileExists = True
					#opens specified file for reading.
					with open(os.path.realpath('.') + '\\orders\\' + date + '.txt', 'r', encoding = 'UTF-8') as e:
						#itterates through every line of the file.
						for line in e.readlines():
							if line[:5] == 'time:':
								clocktime = line[5:].split()
							elif line[:5] == 'road:':
								road = float(line[5:])
							elif line[:6] == 'store:':
								Store = float(line[6:])
							else:
								#keeps track of amount of orders
								lineNum += 1
								#stores everything after the address into a list.
								stuff = line[line.rfind('total') + 6:].split()
								OrderTotal += float(stuff[0])
								#Converts tip into float for calculations.
								OrderTip = float(stuff[2])
								#calculates total amount of tips + mileage.
								tipTotal += OrderTip + 1.4
						tStart = clocktime[0]
						tEnd = clocktime[1]
						#calculates mileage
						mile = lineNum * 1.4
						tip = tipTotal - mile
						avgTipPerRun = tip / float(lineNum)
						#calculates hours worked and hourly wage.
						#changes to military time for easier access.
						tStart = tStart.replace(':', '')
						tEnd = tEnd.replace(':', '')
						tStart = int(tStart)
						tEnd = int(tEnd)
						#detects whether you are day shift or volume.
						if tStart < 1000 & tStart > 700:
							tEnd += 1200
						elif tStart < 700:
							tStart += 1200
							if tEnd < 300:
								tEnd += 2400
							else:
								tEnd += 1200
						else:
							tEnd += 1200
						tEnd -= 20
						test = str(tStart)[2]
						test2 = str(tEnd)[2]
						if int(test) > 3:
						 	tStart += 20
						elif int(test) < 3:
							tStart -= 20
						# if int(tEnd) > 0:
						# 	tEnd += 40
						print(tStart)
						print(tEnd)
						#Calculates total hours and converts it into a float.
						tTotal = tEnd - tStart
						tTotal = str(tTotal)
						tTotal = tTotal.zfill(4)
						tTotal1 = tTotal[:2]
						tTotal2 = tTotal[2:]
						tTotal = tTotal1 + '.' +  tTotal2
						tTotal = float(tTotal)

						avgRunPerHr = float(lineNum) / tTotal
						approxHrWage = (((avgTipPerRun * avgRunPerHr) + (1.25 * avgRunPerHr)) + ((5 * road) + (9.00 * Store)) / tTotal)
						#prints requested totals.
						print('Total tips $%0.2f' % tip)
						print('Total mileage $%0.2f' % mile)
						print('Total tips plus mileage: $%0.2f' % tipTotal)
						print('Total amount pulled for store: $%.02f' % OrderTotal)
						print('Total number of orders: ' + str(lineNum))
						print('Total hours worked: %.02f' % tTotal)
						print('Average tip per run: $%0.2f' % avgTipPerRun)
						print('Average run per hour: %0.2f' % avgRunPerHr)
						print('Approximate Hourly Wage: $%0.2f' % approxHrWage)
						print('Time on road: %0.2f hours' % road)
						print('Time in store %0.2f hours\n' % (Store))
						break
				else:
					fileExists = False	
		if fileExists == False:
			print('Could not find file...\n')
		main()

	#this if statement determines what functions need to be ran.
	ans = input('What would you like to do?\n (Search, Input File, Store, Total)')
	print()
	fileExists = False
	#initiates the search function.
	if ans.lower() == 'search':
		day = input('Enter the date you would like to search trough: ')
		num = input('Enter order number: ')
		print()
		search(day, num)
	#initiates the store function
	elif ans.lower() == 'store':
		Num = input('Order Number: ')
		orderAddress = input('Address: ')
		orderTotal = input('Total: ')
		orderPaid = input('Amount Paid: ')
		print()
		store(Num, orderAddress, orderTotal, orderPaid)
	#initiates the total function.
	elif ans.lower() == 'total':
		date = input('Enter the date you would like to get the total from: ')
		print()
		total(date)
	elif ans.lower() == 'input file':
		loc = input('Enter location of file: ')
		date = input('Enter the date you would like to set this file to: ')
		for root, dirs, filenames in os.walk('.\\orders'):
			for f in filenames:
				if f == (date + '.txt'):
					fileExists - True
					d = input('File already exists, would you like to overwrite it? y/n ')
					print()
					if d.lower() == 'y':
						os.remove('.\\orders\\' + date + '.txt')
						inputFile(loc, date)
		if fileExists == False:
			inputFile(loc, date)
		print()
		

#attempts to open todays file. if it doesnt exist, the file is created and asks for your clock times.
clocktime = False
try:
	with open(os.path.realpath('.') + '\\orders\\' + time.strftime('%m-%d-%y') + '.txt', 'r', encoding = 'UTF-8') as f:
		pass
except FileNotFoundError:
	with open(os.path.realpath('.') + '\\orders\\' + time.strftime('%m-%d-%y') + '.txt', 'a', encoding = 'UTF-8') as f:
		with open(os.path.realpath('.') + '\\orders\\' + time.strftime('%m-%d-%y') + '.txt', 'r+', encoding = 'UTF-8') as h:
			for line in h.readlines():
				if line[:5] == 'time:':
					clocktime = True
		if clocktime == False:
			start = input('Enter clock in time for today:(e.g. 5:30 or 5:00) ')
			end = input('Enter clock out time for today: ')
			road = input('Enter time on road: ')
			Store = input('Enter time in store: ')
			f.write('time: ' + start + ' ' + end + '\n')
			f.write('road: ' + road + '\n')
			f.write('store: ' + Store + '\n')
		h.close()
	f.close()
print()
main()