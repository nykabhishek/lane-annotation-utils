import json
import matplotlib.pyplot as plt
import itertools
import PIL
import Image
import os

os.system('clear')


#use the json groundtruth labels labels file
jsonInputPath = "./bdd100k/labels/bdd100k_labels_images_train.json"
#open a stream to that file to read it.
inputStream = open(jsonInputPath)
#set the max for graphing the images (if you want to graph them that is)
ymax = 720
xmax = 1280
###
#load the input json data into the 'data' variable
with open(jsonInputPath) as inputStream:
	data = json.load(inputStream)
#When converting to CULane, part of what is necessary is a 'control file'.
#this file controls the flow of other programs. It's just the file path_name of 
#the images that are annotated.
#So we'll have to create one as we convert this database.
outputControlPath = './BDDtoCU/list/train.txt'
outputControlStream = open(outputControlPath, 'w+')
###
#loop through each json object in 'data'
for jsonIndex in range(len(data)):
	#reset the coordinates for each picture we process
	coordinates = []
	_x = []
	_y = []
	###
	picture_name = data[jsonIndex]['name']
	
	#outputPath is where the converted coordinates will go
	outputPath = './BDDtoCU/annotations/' + str(picture_name)
	outputPath = outputPath[:-4]
	outputPath += '.lines.txt'
	output_stream = open(outputPath, 'w+')

	picture_pathname = 'bdd100k/images/100k/train/'
	picture_pathname += picture_name
	picture_pathname = str(picture_pathname)

	pictureControlOutput = "/annotations/" + str(picture_name)

	outputControlStream.write(pictureControlOutput)
	outputControlStream.write('\n')
	#the annotations in BDD100K contain a LOT of data. Only some of it is lane data.
	#loop through all the labels they have, and find the lane data. 
	#for every lane data you find, store it into the coordinates array.
	for labelIndex in range(len(data[jsonIndex]['labels'])):
		if(data[jsonIndex]['labels'][labelIndex]['category'] == 'lane'):
			for laneIndex in range(len(data[jsonIndex]['labels'][labelIndex]['poly2d'])):
				helpy = []
				for pointIndex in range(len(data[jsonIndex]['labels'][labelIndex]['poly2d'][laneIndex]['vertices'])):
					helpy.append(data[jsonIndex]['labels'][labelIndex]['poly2d'][laneIndex]['vertices'][pointIndex])
				coordinates.append(helpy)
	#Once you've saved all the lane coordinates for a single image, 
	#We need to unpack them into the CULane format:
	"""
	... need this format first....:
	_x: 
	[[624.156, 590.589, 557.022, 522.496, 488.929, 455.361, 421.794, 387.268, 353.701, 320.134, 285.801, 252.234, 217.707, 184.14, 150.573, 117.006, 82.4794, 48.9122, 15.345, -18.9311], [740.475, 728.142, 715.809, 704.246, 691.913, 679.58, 668.017, 655.684, 643.351, 631.788, 619.455, 607.122, 595.559, 583.226, 571.27, 558.937, 546.603, 535.041, 522.708, 510.374, 498.041, 486.479, 474.145, 461.812, 450.25, 437.916, 425.583, 414.021, 401.58], [821.014, 838.271, 855.529, 872.787, 889.182, 906.439, 923.697, 940.954, 958.212, 974.607, 991.865, 1009.12, 1026.38, 1042.77, 1060.03, 1077.38, 1094.64, 1111.9, 1128.29, 1145.55, 1162.81, 1180.07, 1196.46, 1213.72, 1230.98, 1248.23, 1265.49, 1281.89, 1299.14, 1316.36], [903.131, 954.185, 1006.22, 1058.25, 1109.31, 1161.34, 1213.38, 1264.95, 1316.01, 1368.04, 1420.08, 1471.13, 1523.17, 1575.2, 1626.25, 1678.16]]
	_y: 
	[[270.0, 260.0, 250.0, 240.0, 230.0, 220.0, 210.0, 200.0, 190.0, 180.0, 170.0, 160.0, 150.0, 140.0, 130.0, 120.0, 110.0, 100.0, 90.0, 80.0], [280.0, 270.0, 260.0, 250.0, 240.0, 230.0, 220.0, 210.0, 200.0, 190.0, 180.0, 170.0, 160.0, 150.0, 140.0, 130.0, 120.0, 110.0, 100.0, 90.0, 80.0, 70.0, 60.0, 50.0, 40.0, 30.0, 20.0, 10.0, 0.0], [290.0, 280.0, 270.0, 260.0, 250.0, 240.0, 230.0, 220.0, 210.0, 200.0, 190.0, 180.0, 170.0, 160.0, 150.0, 140.0, 130.0, 120.0, 110.0, 100.0, 90.0, 80.0, 70.0, 60.0, 50.0, 40.0, 30.0, 20.0, 10.0, 0.0], [290.0, 280.0, 270.0, 260.0, 250.0, 240.0, 230.0, 220.0, 210.0, 200.0, 190.0, 180.0, 170.0, 160.0, 150.0, 140.0]]
	"""
	#read, unpack and save the BDD100K lane coordinates into _x and _y
	for lane in coordinates:
		#graph line?
		helpyx = []
		helpyy = []
		for point in lane:
			helpyx.append(point[0])
			helpyy.append(point[1])
		_x.append(helpyx)
		_y.append(helpyy)

	#flip the y coordinates
	for i in range(len(_y)):
		for j in range(len(_y[i])):
			_y[i][j] = ymax - _y[i][j]

	#code block to graph the pictures.
	#uncomment if you're interested in seeing BDD100K graphed with the appropriate
	#image associated with the coordinates.
	'''
	img = Image.open(picture_pathname)
	fig, ax = plt.subplots()
	#flip the image
	img = img.transpose(Image.FLIP_TOP_BOTTOM)
	#show the image
	ax.imshow(img, origin='upper')
	axes = plt.gca()
	#set the limits of the graph/subplot
	axes.set_xlim(0,xmax)
	axes.set_ylim(0,ymax)
	#time to plot
	for i in range(len(_y)):
		plt.plot(_x[i],_y[i],color='red')
	plt.show()
	'''
	
	#output CULANE format:
		#x y x y x y x y
		#x y x y x y
		#x y x y x y x y x y x y 
	#etc.
	for i in range(len(_y)):
		#lane
		for j in range(len(_y[i])):
			output_stream.write(str(_x[i][j]))
			output_stream.write(' ')
			output_stream.write(str(_y[i][j]))
			output_stream.write(' ')
		output_stream.write('\n')


	

