#convert CU to TU

import json
import os
import numpy as numpy
import shutil

#clear the terminal of output:
os.system('clear')
#here's my issue with all these things.
#i think i need to have the input and output be up to the user.
input_folder = "zzzzz1234890-2123454317890!@#$!!@#$"
while(not os.path.exists(input_folder)):
	input_folder = raw_input("please enter the input CULane data foldername: ")
	input_folder = str(input_folder)
	input_folder = "./" + input_folder
	if not os.path.exists(input_folder):
		answer = raw_input("folder not found, try again? (y/n): ")
		if answer == 'n':
			quit()


	#-...
	#folder not found
	#or folder found.
	#what would you like to call the output file containing the TU labels.
	#beginning conversion

#use a file to control what files to convert
input_control_pathname = input_folder + "/list/train.txt"
#open that file. Then for every directory listed in it, we will conver thtat file into a json entry and output it
output_pathname = "./CUtoTU/label_data.json"

#set up the streams for input control and output (input_stream is different than input control_stream)
input_control_stream = open(input_control_pathname, 'r')
output_stream = open(output_pathname, 'w+')
yHeight = 590
#for every pathname in input_control steam, open astream to the file it points to
for current_control in input_control_stream:
	current_control = input_folder + current_control
	picture_pathname = current_control[:-1]
	#print picture_pathname
	#change '.jpg' to '.lines.txt'
	current_control = current_control[:-5]
	current_control = current_control + '.lines.txt'
	#check to see if that file even exists
	#ignore this file if it doesn't exist
	exists = os.path.isfile(current_control)
	if(not exists):
		print current_control + ' not found'
		continue
	#open input stream using current control
	input_stream = open(current_control, 'r')
	#initialize lane_data dictionary
	lane_data = {}
	lane_data['lanes'] = []
	lane_data['h_samples'] = []
	lane_data['raw_file'] = ''

	#build a dictionary using the input_stream to create a json object
	coordinates = []
	_x = []
	_y = []
	for line in input_stream:
		lane = line.split(' ')
		coordinates.append(lane)
		_x.append([])
		_y.append([])
	#break up x and y coordinates from the input stream (it's currently x y x y x y x y)
	c = 'x'
	laneNum = 0
	for i in range(len(coordinates)):
		for j in range(len(coordinates[i])):
			#base case
			if(coordinates[i][j] == '\n'):
				continue
			elif(c == 'x'):
				c = 'y'
				_x[i].insert(0,float(coordinates[i][j]))
			elif(c == 'y'):
				c = 'x'
				_y[i].insert(0,float(coordinates[i][j]))
	#for 'h_samples i'll have to find the miniest min to be min, and the maxiest max to be max
	#find the global min and max
	_yMax = 0
	_yMin = 10000000
	for i in range(len(_y)):
		for j in range(len(_y[i])):
			#find min
			if(_y[i][j] < _yMin):
				_yMin = _y[i][j]
			#find max
			if(_y[i][j] > _yMax):
				_yMax = _y[i][j]
	#once you've found the global min/max:
	#then create h_samples: an array between the min and max, with increments of 10
	y = _yMin
	h_samples = []
	while(y < _yMax + 1):
		h_samples.append(y)
		y = y + 10
	
	#pad the lanes with the necessary amount of '-100s' based on the min max
	for i in range(len(_y)):
		#find the local minimum and maximum
		localMinY = 100000
		localMaxY = 0
		for j in range(len(_y[i])):
			if(_y[i][j] < localMinY):
				localMinY = _y[i][j]
			if(_y[i][j] > localMaxY):
				localMaxY = _y[i][j]
		#'front pass'
		for curMin in range(int(_yMin),int(localMinY),10):
			_x[i].insert(0,-2)
		#'back pass'
		for curMax in range(int(_yMax), int(localMaxY),-10):
			_x[i].append(-2)
	#update the current lane_data object to have all these processed values and then output it
	lane_data['h_samples'] = h_samples
	lane_data['lanes'] = _x
	lane_data['raw_file'] = picture_pathname
	json_object = json.dumps(lane_data)
	output_stream.write(json_object)
	output_stream.write('\n')

