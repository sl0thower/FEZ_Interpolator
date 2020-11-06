from os import system, name
import pandas as pd
import numpy as np

def clearScreen():
	if name == 'nt':
		_ = system('cls') #for windows
	else:
		_ = system('clear') #fow mac

def interpolate(x1,x2,y1,y2,inVal):
	m = (y2-y1)/(x2-x1)
	b = y2 - (m * x2)
	outVal = (m * inVal) + b
	return outVal

def findNeighbours(inVar, inVal):
	exactMatch = airProperties[airProperties[inVar] == inVal]
	if not exactMatch.empty:
		return exactMatch.index
	else:
		lowerVal = airProperties[airProperties[inVar]<inVal][inVar].idxmax()
		upperVal = airProperties[airProperties[inVar]>inVal][inVar].idxmin()
		#lowerVal_loc = airProperties[airProperties[inVar] == lowerVal].index.values
		#upperVal_loc = airProperties[airProperties[inVar] == upperVal].index.values
		return lowerVal, upperVal

unitsStringArray = ['','SI','English']

#start main loop
clearScreen()
print('\n\n' + '  _ ___  ___   ____    ' + '\n' +
               ' | .__/ / _ \ /_  /    ' + '\n' +
               ' | |___   __/  / /__     ' + '\n' +
               ' | .__/ \___/ /_____/    ' + '\n' +
               ' |_|             ' + '\n\n')

#figuring out what table to download. SI or english.
unitsLoop = True
while unitsLoop:
	try:
		units = int(input('Enter the desired units;' + '\n\n' + 
					  '1) SI' + '\n' + 
					  '2) English' + '\n\n' + 
					  '1 or 2: '))
	except ValueError:
		clearScreen()
		print('\nThat\'s not even a number lol\n')
		continue

	if units == 1:
		airProperties = pd.read_table('table_a22_SI.txt', sep='\t')
		unitsLoop = False
		clearScreen()
	elif units == 2:
		airProperties = pd.read_table('table_a22_En.txt', sep='\t')
		unitsLoop = False
		clearScreen()
	else:
		clearScreen()
		print('\nIt\'s a 1 or 2 dude. Not that hard.\n')
		continue

while True:

	#asking user to input the value from which we will interpolate
	request = input('Enter the variable followed by its value (space delimited)\n' + 
					'Accepted variables: [' +
					', '.join(airProperties.columns.values) + ']\n\n' + 
					'Remember you are using [' + unitsStringArray[units] + '] units: ')

	#splitting the entry up into variable and value
	requests = request.split()
	inVar, inVal = str(requests[0]), float(requests[1])

	#testing whether they entered a valid variable
	try:
		airProperties[inVar]
	except:
		clearScreen()
		print('\nYou failed to enter an accepted variable. You fool. Try Again.\n')
		continue

	if inVal in airProperties[inVar].values:
		i = airProperties[inVar].isin([inVal])
		print('\n')
		for var in airProperties.columns.values:
			print(str(var) + ' ' + str(airProperties[var][i].values))
		print('\n')
	else:
		values = []
		x1_loc, x2_loc = findNeighbours(inVar, inVal)
		x1 = airProperties[inVar][x1_loc]
		x2 = airProperties[inVar][x2_loc]
		for outVar in airProperties.columns.values:
			y1 = airProperties.iloc[x1_loc][outVar]
			y2 = airProperties.iloc[x2_loc][outVar]
			outVal = interpolate(x1,x2,y1,y2,inVal)
			tempList = [[outVar, outVal]]
			values = values + tempList

		print('\n')
		for i in range(len(values)):
			print(str(values[i][0]) + ' [' + str(round(values[i][1], 4)) + ']')
		print('\n')

	closingRemarks = input('Press \"Enter\" to find another value.\n' +
						   'Press \"Ctrl-C\" to quit... ')

	if closingRemarks == '':
		clearScreen()
		continue
	else:
		clearScrean()
		break 
