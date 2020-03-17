import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from plate_lighting import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class WellPlot(BoxLayout):
	def __init__(self, **kwargs):
		super(WellPlot, self).__init__(**kwargs)
		A1_X = 0.23
		A1_Y = 0.58
		WELL_SPACING = 0.045
		CIRC_RADIUIS  = 0.023
		self.well_plot = PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING)
		self.add_widget(FigureCanvasKivyAgg(figure=self.well_plot.fig))

class PlateLightingApp(App):
	def build(self):
		p = PLWidget()
		return p
class PLWidget(BoxLayout):
	def __init__(self, **kwargs):
		super(PLWidget, self).__init__(**kwargs)

if __name__ == '__main__':
	Window.fullscreen = True
	PlateLightingApp().run()
