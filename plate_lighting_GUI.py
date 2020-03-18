import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from plate_lighting import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.label import Label

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
		A1_X = 0.23
		A1_Y = 0.58
		WELL_SPACING = 0.045
		CIRC_RADIUIS  = 0.023
		self.pl = PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING)
		self.add_widget(FigureCanvasKivyAgg(figure=self.pl.fig))

class PlateLightingApp(App):
	def build(self):
		p = PLWidget()
		return p

class PLWidget(BoxLayout):
	def __init__(self, **kwargs):
		super(PLWidget, self).__init__(**kwargs)
		self.ids.textbox.bind(focus=on_focus)
		self.plateLighting = self.ids.wellPlot.pl
		self.scanMode = False #enable after name and input have been scanned
		self.ids.textbox.bind(on_text_validate=self.scanName)

	''' CALLBACKS '''

	def scanName(self, *args):
		print('scanName bound')

		# TODO check if valid name tag
		check_input = self.ids.textbox.text
		self.user_name = check_input
		self.ids.user_name_label.text += check_input 
		self.ids.textbox.text = ''

		# bind textbox to scanBarcode after name is scanned
		self.ids.textbox.funbind('on_text_validate',self.scanName)
		self.ids.textbox.bind(on_text_validate=self.scanBarcode)
		self.ids.notificationLabel.text = 'Please scan your plate'

		# self.requestPlate()

		# bind textbox to scanBarcode
	def scanBarcode(self, *args):
		print('scanBarcode bound')
		# TODO check if valid plate barcode @ Spyros
		check_input = self.ids.textbox.text
		self.plate_barcode = check_input
		self.ids.plate_barcode_label.text += check_input 
		self.ids.textbox.text = ''

		self.plateLighting.ttw.openCSV(self.user_name, self.plate_barcode)

		# bind textbox to switchwell after barcode is scanned
		self.ids.textbox.funbind('on_text_validate',self.scanBarcode)
		self.ids.textbox.bind(on_text_validate=self.switchWell)
		self.ids.notificationLabel.text = 'Please scan your tube'

	# def scanMeta(self, *args):

	def switchWell(self, *args):
		check_input = self.ids.textbox.text 
		self.plateLighting.switchWell(check_input)
		self.ids.notificationLabel.text = self.plateLighting.well_dict[check_input].location
		print(self.plateLighting.well_dict[check_input].location)
		self.ids.textbox.text = '' #clear textbox after scan
	
if __name__ == '__main__':
	Window.fullscreen = True
	PlateLightingApp().run()
