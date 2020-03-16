#!/usr/bin/env python3

import argparse
import csv
import time

def main():
	timestr = time.strftime("%Y%m%d-%H%M%S")
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name',  help="input user name", required=True)
	parser.add_argument('-b', '--barcode',  help="barcode number",  required=True)
	args = parser.parse_args()
	print("user: " + args.name)
	print("deep well barcode: " + args.barcode) #this should check if it's a valid plate barcode
	print("date: " + timestr)

	metadata = [['date', timestr], ['name', args.name], ['deep well barcode', args.barcode]]
	
	# the csv filename will be unique from scan time - confirm with Rafael how to decide filename
	with open(timestr+'.csv', 'a', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(metadata)
	# csvFile.close()

	scanned_tubes = []
	check_input = input()

	# the user can only end the protocol by scanning the well plate again, however they cannot end the protocol if there were no tubes scanned
	while check_input != args.barcode or not scanned_tubes:
		# find a way to make sure inputs came from barcode"
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
		check_input = input()
	print('finished')
	
if __name__== "__main__":
  main()
