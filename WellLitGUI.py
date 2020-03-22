# Joana Cabrera
# 3/15/2020

import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from plate_lighting import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import time

class ConfirmPopup(Popup):
	def __init__(self, txt_file_path=None):
		super(ConfirmPopup, self).__init__()
		self.pos_hint={'y': 800 /  Window.height}
		self.txt_file_path = txt_file_path

	def show(self):
		content = BoxLayout(orientation='vertical')
		popup_lb = Label(text='Finish plate?', font_size = 30)
		content.add_widget(popup_lb)
		button_box = BoxLayout(orientation='horizontal', size_hint=(1, .4))
		content.add_widget(button_box)

		# configure yes button
		self.yes_button = Button(text='yes')
		button_box.add_widget(self.yes_button)
		self.yes_button.bind(on_press=self.yes_callback)
		self.yes_button.bind(on_press=self.dismiss)

		# configure no button
		no_button = Button(text='no')
		button_box.add_widget(no_button)
		no_button.bind(on_press=self.dismiss)


		self.content = content
		self.open()
	def yes_callback(self, *args):
		if self.txt_file_path:
			txt_file = open(self.txt_file_path,"w") 
			txt_file.close() 
		WellLitApp.get_running_app().p.resetAll()

class WellLitPopup(Popup):
	def __init__(self):
		super(WellLitPopup, self).__init__()
		self.pos_hint={'y': 800 /  Window.height}

	def show(self,error_str):
		content = BoxLayout(orientation='vertical')
		popup_lb = Label(text=error_str, font_size = 30)
		content.add_widget(popup_lb)
		close_button = Button(text='Close', size_hint=(1, .4))
		content.add_widget(close_button)
		close_button.bind(on_press=self.dismiss)
		self.content = content
		self.open()

class MetaLabel(Label):
	pass

def on_focus(instance, value):
	# refocus on the text box after defocused by the enter key
	if value:
		pass
	else:
		instance.focus = True

class WellPlot(BoxLayout):
	def __init__(self, **kwargs):
		super(WellPlot, self).__init__(**kwargs)
		A1_X = 0.235
		A1_Y = 0.59
		WELL_SPACING = 0.045
		CIRC_RADIUIS  = 0.024
		self.pl = PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING)
		self.add_widget(FigureCanvasKivyAgg(figure=self.pl.fig))
	def on_touch_down(self, touch):
		pass

class WellLitApp(App):
	def build(self):
		self.p = PLWidget()
		return self.p

class PLWidget(BoxLayout):
	def __init__(self, **kwargs):
		super(PLWidget, self).__init__(**kwargs)
		self.ids.textbox.bind(focus=on_focus)
		self.plateLighting = self.ids.wellPlot.pl
		self.scanMode = False #enable after name and input have been scanned
		self.ids.textbox.bind(on_text_validate=self.scanRecorder)
		self.error_popup = WellLitPopup()
		self.canUndo = False
		self.warningsMade = False
		self.confirm_popup = ConfirmPopup()
		
	def makeWarningFile(self):
		# set up path to save warnings
		self.warningsMade = True
		self.warning_file_path = os.path.join(self.plateLighting.ttw.csv_file_path +'_WARNING')
		self.warning_metadata = self.plateLighting.ttw.metadata

		with open(self.warning_file_path + '.csv', 'w', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(self.warning_metadata)
			csvFile.close()

	def undoTube(self):
		# will not enable undo button if there is nothing in scanned tubes or the user has not scanned the plate and barcode
		if not self.canUndo:
			self.error_popup.title =  "Invalid Action"
			self.error_popup.show('Cannot undo')

		elif self.scanMode and self.plateLighting.ttw.scanned_tubes:
			if not self.warningsMade:
				self.makeWarningFile()

			# remove last row from CSV file
			original_rows = []
			with open(self.plateLighting.ttw.csv_file_path+'.csv', 'r') as csvFile:
				reader = csv.reader(csvFile)
				for row in reader:
					original_rows.append(row)
			original_rows_edited = original_rows[:-1]
			with open(self.plateLighting.ttw.csv_file_path + '.csv', 'w', newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerows(original_rows_edited)
				csvFile.close()

			# clear the target on the plate lighting plot
			self.plateLighting.target.markEmpty()
			self.plateLighting.fig.canvas.draw()

			# move back one index the TubeToWell and PlateLighting objects
			self.plateLighting.ttw.scanned_tubes = self.plateLighting.ttw.scanned_tubes[:-1]
			undone_barcode = self.plateLighting.target.barcode
			undone_location = self.plateLighting.ttw.tube_locations[undone_barcode]
			self.plateLighting.ttw.tube_locations[undone_barcode] = ''
			self.plateLighting.well_idx -= 1
			self.plateLighting.ttw.current_idx -=1
			self.canUndo = False # do not allow the user to undo more than once in a row


			# write to warning file
			warn_timestr = time.strftime("%Y%m%d-%H%M%S")
			warning_row = [[warn_timestr, undone_barcode, undone_location, 'unscanned']]
			with open(self.warning_file_path + '.csv', 'a', newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerows(warning_row)
				csvFile.close()

			# show popup confirming that the tube was unscanned
			self.error_popup.title =  "Notification"
			self.ids.tube_barcode_label.text = '' 
			self.error_popup.show('Tube Unscanned')

			self.ids.notificationLabel.font_size = 50
			self.ids.notificationLabel.text = 'Please scan tube'


		else:
			# show popup telling the user they cannot undo
			self.error_popup.title =  "Invalid Action"
			self.error_popup.show('Nothing to undo')
			self.ids.textbox.text = ''

	def finishPlate(self):
		self.confirm_popup.show()
		# self.resetAll()

		# reset PlateLighting object

	def resetAll(self): 
		self.plateLighting.reset()
		
		# restart metadata collection
		self.ids.textbox.funbind('on_text_validate',self.switchWell)
		self.ids.textbox.funbind('on_text_validate',self.scanAliquoter)
		self.ids.textbox.funbind('on_text_validate',self.scanPlate)
		self.ids.textbox.bind(on_text_validate=self.scanRecorder)
		self.ids.notificationLabel.text = "Please scan the recorder's barcode"

		# reset metadata text
		self.ids.recorder_label.text = '[b]Recorder:[/b] \n'
		self.ids.aliquoter_label.text = '[b]Aliquoter:[/b] \n'
		self.ids.plate_barcode_label.text = '[b]Plate Barcode:[/b] \n'
		self.ids.tube_barcode_label.text = '[b]Tube Barcode:[/b] \n'
		self.ids.notificationLabel.font_size = 50

		self.scanMode = False
		self.canUndo = False
		self.warningsMade = False

	def showBarcodeError(self, barcode_type):
		self.error_popup.title =  "Barcode Error"
		self.error_popup.show('Not a valid ' + barcode_type +' barcode')
		self.ids.textbox.text = ''

	def scanRecorder(self, *args):
		check_input = self.ids.textbox.text
		if self.plateLighting.ttw.isName(check_input):
			self.recorder = check_input
			self.ids.recorder_label.text += check_input 
			self.ids.textbox.text = ''

			# bind textbox to scanPlate after name is scanned
			self.ids.textbox.funbind('on_text_validate',self.scanRecorder)
			self.ids.textbox.bind(on_text_validate=self.scanAliquoter)
			self.ids.notificationLabel.text = "Please scan the aliquoter's barcode"
		else: 
			self.showBarcodeError('name')

	def scanAliquoter(self, *args):
		check_input = self.ids.textbox.text
		if self.plateLighting.ttw.isName(check_input):
			self.aliquoter = check_input
			self.ids.aliquoter_label.text += check_input 
			self.ids.textbox.text = ''

			# bind textbox to scanPlate after name is scanned
			self.ids.textbox.funbind('on_text_validate',self.scanAliquoter)
			self.ids.textbox.bind(on_text_validate=self.scanPlate)
			self.ids.notificationLabel.text = 'Please scan plate'
		else: 
			self.showBarcodeError('name')

		# bind textbox to scanPlate
	def scanPlate(self, *args):
		check_input = self.ids.textbox.text
		if self.plateLighting.ttw.isPlate(check_input):
			self.plate_barcode = check_input
			self.ids.plate_barcode_label.text += check_input 
			self.ids.textbox.text = ''

			# openCSV 
			self.plateLighting.ttw.openCSV(recorder=self.recorder, aliquoter=self.aliquoter, plate_barcode=self.plate_barcode)

			# set up text file confirmation
			self.txt_file_path = os.path.join(self.plateLighting.ttw.csv_file_path +'_FINISHED.txt')
			self.confirm_popup = ConfirmPopup(self.txt_file_path)

			# bind textbox to switchwell after barcode is scanned
			self.ids.textbox.funbind('on_text_validate',self.scanPlate)
			self.ids.textbox.bind(on_text_validate=self.switchWell)

			self.ids.notificationLabel.text = 'Please scan tube'
			self.scanMode = True

		else: 
			self.showBarcodeError('plate')

	def switchWell(self, *args):
		check_input = self.ids.textbox.text 

		# switch well if it is a new tube
		if self.plateLighting.ttw.isTube(check_input):
			self.ids.tube_barcode_label.text = check_input
			self.canUndo = self.plateLighting.switchWell(check_input) # can only undo if it's a new target
			self.ids.notificationLabel.font_size = 100
			self.ids.notificationLabel.text = self.plateLighting.well_dict[check_input].location
			print(self.plateLighting.well_dict[check_input].location)
			self.ids.textbox.text = '' #clear textbox after scan
		else: 
			self.showBarcodeError('tube')
		
if __name__ == '__main__':
	Window.size =(1600,1200)
	Window.fullscreen = True
	WellLitApp().run()
