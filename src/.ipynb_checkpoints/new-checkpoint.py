import ann_visualizer as av

# color palette
LGT_VAL = "#d7eaf3"
MID_VAL = "#77b5d9"
DRK_VAL = "#14397d"

TMP_IMG_FILENAME = "tempImage.png"
# https://commons.wikimedia.org/wiki/File:Cajal_cortex_drawings.png
# https://upload.wikimedia.org/wikipedia/commons/5/5b/Cajal_cortex_drawings.png
# User:Looie496 created file,
# Santiago Ramon y Cajal created artwork [Public domain]

def main():
	viz = av.Visualizer(pattern = [4, 10, 7, 5, 8])
	
	viz.setColor(LGT_VAL, MID_VAL, DRK_VAL)
	viz.loadTempImage(TMP_IMG_FILENAME)
	viz.createInputNodes()
	viz.createLayerNodes()
	viz.createOutputNode()
	viz.createErrorNode()
	# TODO: create layer connections
	
	viz.exportImage("newViz.png")
    
if __name__ == "__main__":
    main()