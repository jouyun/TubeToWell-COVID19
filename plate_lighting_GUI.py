import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from plate_lighting import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window

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

	''' CALLBACKS '''
	def switchWell(self):
		check_input = self.ids.textbox.text 
		self.plateLighting.switchWell(check_input)
		# print(self.plateLighting.ttw.tube_locations[check_input])
		# self.ids.test_display.text = self.plateLighting.well_dict[check_input]
		self.ids.textbox.text = '' #clear textbox after scan
	
if __name__ == '__main__':
	Window.fullscreen = True
	PlateLightingApp().run()
