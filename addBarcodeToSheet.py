
# Paul Lebel
# 2020/03/18

# 1. Reads in a .csv file that has a column labeled 'Accession Number'
# 2. Reads the accession numbers from the .csv file
# 3. Creates a barcode image from each accession number
# 4. Writes a new .xls file with the barcode images added to each row

import os,sys, getopt
import csv
import barcode
import xlsxwriter
from barcode.writer import ImageWriter


def addBarcodeToSheet(csvFullFilenames: list, \
	headerRows: int = 4, \
	barcodeCol: int = 1, \
	cellWidth: int  = 25, \
	cellHeight: int = 110, \
	scale: float = 0.5, \
	barcodeType: str = 'code39', \
	*args, \
	**kwargs):

	# This function reads in a .csv file, goes through it line-by-line and 
	# copies it over to a .xlsx file. While doing so, it reads a barcode
	# accession number (specified by barcodeCol), and produces a barcode
	# image from it. Each barcode image is inserted into a new column on the 
	# right of the sheet. The image is configured to re-size with the
	# cell, however this doesn't seem to work for me. 

	# Input args:
	# csvFullFilenames: a list of absolute (or local) filenames to the .csv files to process

	# All other input arguments are optional and can be used either as positional 
	# or keyword args

	# headerRows: Number of rows in header (copies them over but otherwise skips them)
	# barcodeCol: index to the column containing the barcodes
	# cellWidth / cellHeight: dimensions of the cell in which to insert the images
	# scale: Scale factor for the barcode images
	# barcodeType: String coding for the barcode type

	for csvFName in csvFullFilenames:
		try: 
			csvFile = open(csvFName,'r')
		except OSError:
			print('Could not open/read file')
			sys.exit()

		with csvFile:
			reader = csv.reader(csvFile)

			# This should have three components: path, filename, extension
			fParts = os.path.split(csvFName)

			# Split the extension out
			filename, file_extension = os.path.splitext(fParts[-1])

			# Create a new path that is for the new excel file
			fullXLSPath = os.path.join(fParts[0], filename + '.xlsx')
			workbook = xlsxwriter.Workbook(fullXLSPath)
			worksheet = workbook.add_worksheet()

			rowInd = 0
			imgFilenames = []
			for row in reader:

				# Copy over the existing sheet cell entries
				for colInd in range(len(row)):
					worksheet.write(rowInd, colInd, row[colInd])

				# Write the column header for the barcode image
				if rowInd == headerRows-1:
					worksheet.write(rowInd, colInd+1, 'Barcode Image')

				# Create the barcode and add it to the sheet
				if rowInd >= headerRows:
					ean = barcode.get(barcodeType, row[barcodeCol], writer=ImageWriter())
					imgFilenames.append(ean.save(os.path.join(fParts[0],row[barcodeCol])))
					worksheet.insert_image(rowInd, colInd+1,imgFilenames[-1], \
						{'x_scale': scale, 'y_scale': scale, 'object_position': 1})

					worksheet.set_column(rowInd, colInd+1, cellWidth)
					worksheet.set_row(rowInd, cellHeight)
				rowInd += 1
			workbook.close()
			
			# Remove the images at the end because the worksheet needs to close before 
			# the images are deleted.
			for img in imgFilenames:
				os.remove(img)


if __name__ == '__main__':
	addBarcodeToSheet(sys.argv[1:])