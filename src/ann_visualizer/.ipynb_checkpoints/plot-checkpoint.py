import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

class Plot:
	def __init__(self, width, height, margin):
		self._fig = plt.figure(figsize = (width, height))
		
		self._axMain = self._fig.add_axes((0, 0, 1, 1), facecolor = "none")
		self._axMain.set_xlim(0, 1)
		self._axMain.set_ylim(0, 1)
		
		self._margin = margin

	##################################################
	################# public methods #################
	##################################################
	def setPlotColor(self, faceColor, edgeColor):
		self._fig.set_facecolor(faceColor)
		self._fig.set_edgecolor(edgeColor)
		
	def getAxMain(self):
		return self._axMain
	
	def getContextHeight(self):
		return self._fig.get_figheight() - (self._margin * 2)
	
	def getContextWidth(self):
		return self._fig.get_figwidth() - (self._margin * 2)

	def getFig(self):
		return self._fig

	def getMargin(self):
		return self._margin

	def getTotalHeight(self):
		return self._fig.get_figheight()

	def getTotalWidth(self):
		return self._fig.get_figwidth()

