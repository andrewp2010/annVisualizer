from .plot import Plot
from .layer import Layer

import numpy as np
from os import path
from PIL import Image

class Visualizer:
	##################################################
	############### constant variables ###############
	##################################################	
	_TEMP_IMAGE_DEFAULT_SCALE = 3

	def __init__(self, width = 16, height = 9, margin = 0.5, nodeAspectRatio = 1.33, gapScale = 0.5, ioLayerScale = 0.175):
		self._layers = []
		self._plot = Plot(width, height, margin)
		
		self._lgtColor = "#FFFFFF" # white
		self._midColor = "#808080" # grey
		self._drkColor = "#000000" # black
		self._plot.setPlotColor(self._midColor, self._lgtColor)
		
		self._gapScale = gapScale
		self._ioLayerScale = ioLayerScale
		self._layerGap = 0.0
		self._nodeAspectRatio = nodeAspectRatio
		
		self._tempImage = np.zeros((self._TEMP_IMAGE_DEFAULT_SCALE, int(self._TEMP_IMAGE_DEFAULT_SCALE * nodeAspectRatio)))		

##################################################
################# public methods #################
##################################################
	def createInputLayer(self, numNodes):
		inputLayer = Layer(self._plot.getFig())
		self._layers.insert(0, inputLayer)
		
		inputLayerCenter = self._plot.getMargin() + (self._getIoLayerWidth() / 2)
		inputLayer.setCenter(inputLayerCenter)
		
		inputLayerWidth = self._getIoLayerWidth()
		inputLayer.setWidth(inputLayerWidth)

		inputNodeHeight = self._getDynamicNodeHeight(inputLayerWidth, numNodes)
		self._generateLayerNodeParameters(inputLayer, inputNodeHeight)
		
		self._initializeLayerNodes(numNodes, inputLayer)
		self._setNodeImage(inputLayer)

	def createFunctionLayer(self, pattern):
		maxNodes = np.max(pattern)
		
		functionLayerCenter = self._plot.getMargin() + self._getIoLayerWidth()
		functionLayerWidth = self._getFunctionLayerWidth(len(pattern))
		functionNodeHeight = self._getDynamicNodeHeight(functionLayerWidth, maxNodes)
		
		for layerNum in range(len(pattern)):
			numNodes = pattern[layerNum]
			functionLayer = Layer(self._plot.getFig())
			self._layers.append(functionLayer) #TODO: make suer these are always placed in order after input and before output
			
			layerGap = functionLayerWidth * self._gapScale
			if (layerNum == 0):
				functionLayerCenter += layerGap + (functionLayerWidth / 2)
			else:
				functionLayerCenter += layerGap + functionLayerWidth
			functionLayer.setCenter(functionLayerCenter)
			
			functionLayer.setWidth(functionLayerWidth)
			self._generateLayerNodeParameters(functionLayer, functionNodeHeight)
			
			self._initializeLayerNodes(numNodes, functionLayer)
			self._setNodeImage(functionLayer)

	def createLayerNodeConnections(self):
		for currLayer in range(len(self._layers) - 1):
			numStartNodes = self._layers[currLayer].getNumNode()
			numEndNodes = self._layers[currLayer + 1].getNumNode()

			xStart = self._layers[currLayer].getNodes()[0].get_position().x1
			xEnd = self._layers[currLayer + 1].getNodes()[0].get_position().x0

			for nodeStartNum, nodeStart in enumerate(self._layers[currLayer].getNodes()):
				nodeStartPos = nodeStart.get_position()
				yStartMin = nodeStartPos.y0
				yStartMax = nodeStartPos.y1
				startSpace = (yStartMax - yStartMin) / (numEndNodes + 1)

				for nodeEndNum, nodeEnd in enumerate(self._layers[currLayer + 1].getNodes()):
					nodeEndPos = nodeEnd.get_position()
					yEndMin = nodeEndPos.y0
					yEndMax = nodeEndPos.y1
					endSpace = (yEndMax - yEndMin) / (numStartNodes + 1)

					yStart = yStartMin + startSpace * (nodeEndNum + 1)
					yEnd = yEndMin + endSpace * (nodeStartNum + 1)

					self._plotConnections(xStart, xEnd, yStart, yEnd)
				
	def createOutputLayer(self, errorNode = True, errorNodeScale = 0.5):
		outputLayer = Layer(self._plot.getFig())
		self._layers.append(outputLayer)
				
		outputLayerCenter = self._plot.getTotalWidth() - self._plot.getMargin() - (self._getIoLayerWidth() / 2)
		outputLayer.setCenter(outputLayerCenter)
		
		outputLayerWidth = self._getIoLayerWidth()
		outputLayer.setWidth(outputLayerWidth)
		
		outputNodeHeight = outputLayerWidth / self._nodeAspectRatio
		
		self._generateLayerNodeParameters(outputLayer, outputNodeHeight)
		self._initializeLayerNodes(1, outputLayer)
		self._setNodeImage(outputLayer)
		
		if (errorNode):
			self._createErrorNode(outputLayer, errorNodeScale)

	def exportImage(self, filename, usrDpi = 300):
		fig = self._plot.getFig()
		
		fig.savefig(
			filename,
			facecolor = fig.get_facecolor(),
			edgecolor = fig.get_edgecolor(),
			dpi = usrDpi
		)
			
	def loadTempImage(self, filename):
		tmpImgFile = self._getRootDir() + "\\img\\" + filename
		img = Image.open(tmpImgFile)
		img.load()
		
		self._tempImage = np.asarray(img, dtype = "int32")
			
	def setColor(self, lgtColor = "#FFFFFF", midColor = "#808080", drkColor = "#000000"):
		# check is user defined color variables
		if (lgtColor != "#FFFFFF"): self._lgtColor = lgtColor
		if (midColor != "#808080"): self._midColor = midColor
		if (drkColor != "#808080"): self._drkColor = drkColor
		
		self._plot.setPlotColor(self._midColor, self._lgtColor)
		
	##################################################
	################# private methods ################
	##################################################
	def _createErrorNode(self, outputLayer, errorNodeScale):
		outputNodePos = outputLayer.getNodePos(0)
		
		nodeWidth = outputNodePos[2] * errorNodeScale
		nodeHeight = outputNodePos[3] * errorNodeScale
		
		nodeLeft = outputNodePos[0] + (nodeWidth / 2)
		nodeBottom = outputNodePos[1] - nodeHeight - (nodeHeight * self._gapScale)
		
		absPos = [nodeLeft, nodeBottom, nodeWidth, nodeHeight]
		
		outputLayer.createCustomNode(absPos, self._drkColor)
		self._setCustomNodeImage(outputLayer)
	
	def _generateLayerNodeParameters(self, layer, nodeHeight):
		layer.setNodeHeight(nodeHeight)
		layer.setNodeWidth(nodeHeight * self._nodeAspectRatio)
		layer.setNodeGap(nodeHeight * self._gapScale)
		
	def _getDynamicNodeHeight(self, layerWidth, numNodes):
		nodeHeight = layerWidth / self._nodeAspectRatio
		nodeVertSpace = (nodeHeight * numNodes)
		nodeGapSpace = (nodeHeight * self._gapScale * (numNodes - 1))
		if (nodeVertSpace + nodeGapSpace > self._plot.getContextHeight()):
			scaleRatio = self._plot.getContextHeight() / (nodeVertSpace + nodeGapSpace)
			nodeHeight = nodeHeight * scaleRatio
		
		return nodeHeight
			
	def _getFunctionLayerWidth(self, numLyr):
		return (self._plot.getContextWidth() - (self._ioLayerScale * self._plot.getTotalWidth() * 2)) / (self._gapScale + (numLyr * (self._gapScale + 1)))
	
	def _getIoLayerWidth(self):
		return self._ioLayerScale * self._plot.getTotalWidth()
			
	def _getRootDir(self):
		filePath = path.dirname(path.realpath(__file__))
		root, _ = path.split(filePath)
		return root		
	
	def _getTempImage(self):
		rowRatio = int(self._plot.getTotalHeight()) * self._TEMP_IMAGE_DEFAULT_SCALE
		colRatio = int(rowRatio *self._nodeAspectRatio)
		
		top = np.random.randint(self._tempImage.shape[0] - rowRatio + 1)
		bottom = top + rowRatio
		left = np.random.randint(self._tempImage.shape[1] - colRatio + 1)
		right = left + colRatio
		
		tempImage = self._tempImage[top : bottom, left : right]
		
		return tempImage
	
	def _initializeLayerNodes(self, numNodes, layer):
		for i in range(numNodes):
			layer.createNode(self._drkColor)
		layer.setNodePositions()
		
	def _plotConnections(self, x0, x1, y0, y1):
		weight = np.random.sample() * 2 - 1

		x = np.linspace(x0, x1, num = 50)
		y = y0 + (y1 - y0) * (-np.cos(np.pi * (x - x0) / (x1 - x0)) + 1) / 2

		if weight > 0:
			connColor = self._lgtColor
		else:
			connColor = self._drkColor

		self._plot.getAxMain().plot(x, y, color = connColor, linewidth = 2 * weight)
		
	def _setCustomNodeImage(self, layer):
		nodeImages = []
		for i in range(layer.getNumNode()):
			nodeImages.append(self._getTempImage())
		layer.setCustomNodeImages(nodeImages)
		
	def _setNodeImage(self, layer):
		nodeImages = []
		for i in range(layer.getNumNode()):
			nodeImages.append(self._getTempImage())
		layer.setNodeImages(nodeImages)