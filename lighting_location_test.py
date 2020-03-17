import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import matplotlib as mpl


class TargetCircle:
	def __init__(self):
		mpl.rcParams['toolbar'] = 'None'
		plt.style.use('dark_background')
		self.fig, self.ax = plt.subplots()
		self.fig.tight_layout()
		self.ax.axis('equal')
		self.ax.axis('off')
		# self.fig.canvas.manager.full_screen_toggle()

		self.circ = Circle((0.25, 0.43), 0.026, color='red')
		self.ax.add_artist(self.circ)
		self.ax.set_title('Click to move the circle')

		self.fig.canvas.mpl_connect('button_press_event', self.on_click)

	def on_click(self, event):
		if event.inaxes is None:
			return
		self.circ.set_color('green')
		self.circ.center = event.xdata, event.ydata
		print(self.circ.center)
		# print(self.circ.color)
		self.fig.canvas.draw()

	def show(self):
		
		plt.show()


# TargetCircle().show()