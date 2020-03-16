#!/usr/bin/env python3

import argparse
import csv
import time

def main():
	# at startup ask for the user name and well barcode
	timestr = time.strftime("%Y%m%d-%H%M%S")
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name',  help="input user name", required=True)
	parser.add_argument('-b', '--barcode',  help="barcode number",  required=True)
	args = parser.parse_args()
	print("user: " + args.name)
	print("deep well barcode: " + args.barcode) #this should check if it's a valid plate barcode
	print("date: " + timestr)
	metadata = [['date', timestr], ['name', args.name], ['deep well barcode', args.barcode]]

	# make a list of the well row characters
	well_rows = [chr(x) for x in range(ord('A'), ord('H') + 1)]
	# make a list of well names in column wise order 
	well_names = []
	for letter in well_rows:
		for i in range(1,13):
			well_names.append(letter+str(i))
	well_names_iterator = iter(well_names)

	# make a dictionary with the tube locations as the key and the barcodes as the value
	tube_locations = {}
	for w in well_names:
		tube_locations[w] = None

	# the csv filename will be unique from scan time - confirm with Rafael how to decide filename
	with open(timestr+'.csv', 'a', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(metadata)
	# csvFile.close()

	scanned_tubes = []
	check_input = input()

	# the user can only end the protocol by scanning the well plate again, however they cannot end the protocol if there were no tubes scanned
	while check_input != args.barcode or not scanned_tubes:
		# find a way to make sure inputs came from barcode
		# check if the barcode was already scanned
		if check_input == args.barcode:
			print('this is the plate barcode')
		elif check_input in scanned_tubes:
			print('this tube was already scanned')
			# light up corresponding well
		# write to csv if it is a new barcode
		else: 
			with open(timestr+'.csv', 'a', newline='') as csvFile:
				row = [[check_input]]
				writer = csv.writer(csvFile)
				writer.writerows(row)
				scanned_tubes.append(check_input)
				tube_locations[next(well_names_iterator)] = check_input
		check_input = input()
	print('finished')
	
if __name__== "__main__":
  	main()
