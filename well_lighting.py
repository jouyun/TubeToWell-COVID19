import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import matplotlib as mpl

# put this into a state machine later
# if layout changes, use lighting location to find A1 and spacing
A1_X = 0.23
A1_Y = 0.41
WELL_SPACING = 0.045
CIRC_RADIUIS  = 0.026


class WellCircle:
	def __init__(self, center, radius):
		self.empty = True
		self.target = False
		self.center = center
		self.radius = radius
		self.circle = Circle(self.center, self.radius, color='blue', zorder=0)

	def markEmpty(self):
		self.empty = True
		self.target = False
		self.circle.set_color('blue')
		# return self.circle

	def markFilled(self):
		self.empty = False
		self.target = False
		self.circle.set_color('red')
		# return self.circle

	def markTarget(self):
		self.target = True
		self.circle.set_color('yellow')
		self.circle.zorder=1
		# return self.circle

#circle coordinates
def circleCoords(well_spacing, circ_radius):
	# returns a list with all the points in the order to be accessed (column-wise)
	ordered_points = []
	for x in range(12):
		x_coord = A1_X + well_spacing*x
		for y in range(8):
			y_coord = A1_Y - well_spacing*y
			ordered_points.append((x_coord, y_coord))
	return ordered_points
	


class PlateLighting:
	def __init__(self, a1_x, a1_y, circ_radius, well_spacing):

		# set up plot 
		mpl.rcParams['toolbar'] = 'None'
		plt.style.use('dark_background')
		self.fig, self.ax = plt.subplots()
		self.fig.tight_layout()
		self.ax.axis('equal')
		self.ax.axis('off')
		self.fig.canvas.manager.full_screen_toggle() # make sure to set the well lighting display as the main display (go to windows display setting)

		# draw all the empty wells
		self.wells = []
		for x in range(12):
			x_coord = a1_x + (well_spacing * x)
			for y in range(8):
				y_coord = a1_y - (well_spacing * y)
				well = WellCircle((x_coord,y_coord), circ_radius)
				self.wells.append(well)
				self.ax.add_artist(well.circle)
		# print(self.wells)

		# self.target_well_idx = 0
		# self.target_well = self.wells[self.target_well_idx]
		self.wells_iterator = iter(self.wells)

		self.fig.canvas.mpl_connect('button_press_event', self.on_click)

	def on_click(self, event):
		if event.inaxes is None:
			return

		target = next(self.wells_iterator)
		target.markTarget()
		self.fig.canvas.draw()
		target.markFilled()

	def show(self):
		plt.show()


PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()