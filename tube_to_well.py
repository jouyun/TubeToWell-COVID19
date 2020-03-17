#!/usr/bin/env python3

import argparse
import csv
import time 
import os

class TubeToWell:
	def __init__(self):

		# at startup ask for the user name and well barcode
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		self.barcode = 'testbarcode'
		self.name = 'testname'

		# TODO: implement parser equivalent on Kivy
		# self.parser = argparse.ArgumentParser()
		# self.parser.add_argument('-n', '--name',  help="input user name", required=True)
		# self.parser.add_argument('-b', '--barcode',  help="barcode number",  required=True)
		# self.args = self.parser.parse_args()
		# print("user: " + self.args.name)

		print("deep well barcode: " + self.barcode) # TODO: this should check if it's a valid plate barcode (can we get a list of barcodes before hand?)
		print("date: " + self.timestr) 
		self.metadata = [['date', self.timestr], ['name', self.name], ['deep well barcode', self.barcode]] 

		# set up path to save the well locations csv
		self.cwd = os.getcwd()
		self.csv_folder_path = os.path.join(self.cwd, 'well_locations_csv') # TODO: check if folder exists and make it
		self.csv_file_path = os.path.join(self.csv_folder_path, self.timestr + '-' + self.barcode)

		# make a list of the well row characters
		self.well_rows = [chr(x) for x in range(ord('A'), ord('H') + 1)] # move to state machine
		
		# make a list of well names in column wise order 
		self.well_names = []
		for i in range(1,13):
			for letter in self.well_rows:
				self.well_names.append(letter+str(i))
		self.well_names_iterator = iter(self.well_names)

		# make a dictionary with the tube locations as the key and the barcodes as the value
		self.tube_locations = {}
		for w in self.well_names:
			self.tube_locations[w] = None

		# the csv filename will be unique from scan time - TODO: confirm with Rafael how to decide filename
		with open(self.csv_file_path + '.csv', 'a', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(self.metadata)

		self.scanned_tubes = []

	def checkBarcode(self, check_input):
		print('barcode:' + check_input)

		# the user can only end the protocol by scanning the well plate again, however they cannot end the protocol if there were no tubes scanned
		# while check_input != self.args.barcode or not self.scanned_tubes:
			# find a way to make sure inputs came from barcode
		# check if the barcode was already scanned
		if check_input == self.barcode:
			print('this is the plate barcode')
			return False
		elif check_input in self.scanned_tubes:
			print('this tube was already scanned')
			return False
			# light up corresponding well
		else: 
			# write to csv if it is a new barcode
			with open(self.csv_file_path +'.csv', 'a', newline='') as csvFile:
				# log scan time
				scan_time = time.strftime("%Y%m%d-%H%M%S")
				location = next(self.well_names_iterator)
				row = [[scan_time, check_input, location]]
				writer = csv.writer(csvFile)
				writer.writerows(row)

			# add to barcode to scanned_tubes list
			self.scanned_tubes.append(check_input)

			# link barcode to a well location
			self.tube_locations[location] = check_input
			print (location)
			return True

