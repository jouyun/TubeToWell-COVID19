#!/usr/bin/env python3

import argparse
import csv
import time 
import os
import re

class TubeToWell:
	""" A class for mapping scanned tubes to a well location. 

	"""
	def __init__(self):

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

		self.scanned_tubes = []

	def openCSV(self, user_name, plate_barcode): 
		# set up path to save the well locations csv
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		self.cwd = os.getcwd()
		self.csv_folder_path = os.path.join(self.cwd, 'well_locations_csv') # TODO: check if folder exists and make it
		self.csv_file_path = os.path.join(self.csv_folder_path, self.timestr + '_' + plate_barcode)

		self.metadata = [['Timestamp', 'Accession Number', 'Location', 'User Name: ' + user_name, 'Plate Barcode: ' + plate_barcode]]

		# the csv filename will be unique from scan time - TODO: confirm with Rafael how to decide filename
		with open(self.csv_file_path + '.csv', 'a', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(self.metadata)
		self.barcode = plate_barcode

	def isPlate(self, check_input):
		if re.match(r'[RP]{2}[0-9]{6}$', b):
			return True
		else: 
			return False

	def isName(self, check_input):
		pass
	def isTube(self, check_input):
		pass


	def checkTubeBarcode(self, check_input):

		# check if the barcode was already scanned
		if check_input in self.scanned_tubes:
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
			# print (location)
			return location

