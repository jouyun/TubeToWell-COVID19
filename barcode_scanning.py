#!/usr/bin/env python3

import argparse
import csv
import time

def main():
	timestr = time.strftime("%Y%m%d")
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name',  help="input user name", required=True)
	parser.add_argument('-b', '--barcode',  help="barcode number",  required=True)
	args = parser.parse_args()
	print("user: " + args.name)
	print("deep well barcode: " + args.barcode)
	print("date: " + timestr)

	metadata = [['date', timestr], ['name', args.name], ['deep well barcode', args.barcode]]
	with open(timestr+'.csv', 'a', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(metadata)
	# csvFile.close()

	check_input = input()
	while check_input != 'done':
		# find a way to make sure inputs came from barcode"
		with open(timestr+'.csv', 'a', newline='') as csvFile:
			writer = csv.writer(csvFile)
			row = [[check_input]]
			writer.writerows(row)
		check_input = input()
	
if __name__== "__main__":
  main()
