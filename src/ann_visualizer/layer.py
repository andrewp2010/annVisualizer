class Layer:
	def __init__(self, fig):
		self._fig = fig
		self._nodes = []
		self._numNode = 0
		self._customNodes = []
		self._numCustomNode = 0

		self._center = -1.0
		self._height = fig.get_figheight()
		self._width = -1.0
		
		self._nodeGap = -1.0
		self._nodeHeight = -1.0
		self._nodeWidth = -1.0

	##################################################
	################# public methods #################
	##################################################
	def createCustomNode(self, absPos, color):
		relPos = self._calcRelPos(absPos)
		
		node = self._fig.add_axes(relPos)
		self._initializeNodeParams(node, color)
		self._customNodes.append(node)
		self._numCustomNode += 1
		
	def createNode(self, color):
		node = self._fig.add_subplot()
		self._initializeNodeParams(node, color)
		self._nodes.append(node)
		self._numNode += 1
		
	def getNodePos(self, index):
		node = self._nodes[index]
		return self._calcAbsPos(node.get_position())
	
	def getNodes(self):
		return self._nodes
	
	def getNumNode(self):
		return self._numNode
		
	def setCenter(self, center):
		self._center = center
		
	def setCustomNodeImages(self, nodeImages):
		for nodeNum in range(self._numCustomNode):
			self._customNodes[nodeNum].imshow(nodeImages[nodeNum], cmap = "inferno")
		
	def setHeight(self, height):
		self._height = height
		
	def setNodeGap(self, nodeGap):
		self._nodeGap = nodeGap
		
	def setNodePositions(self):
		self._parameterErrorCheck()
		
		nodeLeft = self._center - (self._nodeWidth / 2)
		nodeBottom = (self._height - (self._nodeHeight * self._numNode) - (self._nodeGap * (self._numNode - 1))) / 2
		
		for nodeNum in range(self._numNode):
			absPos = [nodeLeft, nodeBottom, self._nodeWidth, self._nodeHeight]
			relPos = self._calcRelPos(absPos)
			self._nodes[nodeNum].set_position(relPos)
			
			nodeBottom += self._nodeHeight + self._nodeGap
		
	def setNodeHeight(self, nodeHeight):
		self._nodeHeight = nodeHeight
		
	def setNodeImages(self, nodeImages):
		for nodeNum in range(self._numNode):
			self._nodes[nodeNum].imshow(nodeImages[nodeNum], cmap = "inferno")
		
	def setNodeWidth(self, nodeWidth):
		self._nodeWidth = nodeWidth
		
	def setWidth(self, width):
		self._width = width
		self._nodeWidth = width
		
	##################################################
	################# private methods ################
	##################################################
	def _calcAbsPos(self, bbox):
		return [
			bbox.x0 * self._fig.get_figwidth(),
			bbox.y0 * self._fig.get_figheight(),
			(bbox.x1 * self._fig.get_figwidth()) - (bbox.x0 * self._fig.get_figwidth()),
			(bbox.y1 * self._fig.get_figheight()) - (bbox.y0 * self._fig.get_figheight())
		]
		
	def _calcRelPos(self, absPos):
		return [
			absPos[0] / self._fig.get_figwidth(),
			absPos[1] / self._fig.get_figheight(),
			absPos[2] / self._fig.get_figwidth(),
			absPos[3] / self._fig.get_figheight()
		]
	
	def _initializeNodeParams(self, node, color):
		node.tick_params(left = False, right = False, top = False, bottom = False)
		node.tick_params(labelleft = False, labelright = False, labeltop = False, labelbottom = False)
		
		node.spines["left"].set_color(color)
		node.spines["right"].set_color(color)
		node.spines["top"].set_color(color)
		node.spines["bottom"].set_color(color)
		
	def _parameterErrorCheck(self):
		if (self._center < 0.0): raise ValueError("Unable to set node positions. Layer center not defined.")
		if (self._width < 0.0): raise ValueError("Unable to set node positions. Layer width not defined.")
		
		if (self._nodeWidth < 0.0): raise ValueError("Unable to set node positions. Layer node width not defined.")
		if (self._nodeHeight < 0.0): raise ValueError("Unable to set node positions. Layer node height not defined.")
		if (self._nodeGap < 0.0): raise ValueError("Unable to set node positions. Layer node gap not defined.")