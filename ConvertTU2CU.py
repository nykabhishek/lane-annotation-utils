#take the tu format, turn it into CU format.
#tu starts with json
#so i'm taking a .json file and turning it into thousands of .lines.txt files

import json
import os

os.system('clear')

input_folder = "zzzzz1234890-2123454317890!@#$!!@#$"

while(not os.path.exists(input_folder)):
	input_folder = raw_input("please enter the input TUSimple data foldername: ")
	input_folder = str(input_folder)
	input_folder = "./" + input_folder
	if not os.path.exists(input_folder):
		answer = raw_input("folder not found, try again? (y/n): ")
		if answer == 'n':
			quit()


jsonInputPath = input_folder + "/test_label.json"
input_Stream = open(jsonInputPath, 'r')
outputControlPath = './TUtoCU/list/train.txt'
outputControlStream = open(outputControlPath, 'w+')

for line in input_Stream:
	data = json.loads(line)
	imageName = data['raw_file']
	imageName = imageName.split('/')
	imageName = imageName[-1]
	output_pathname = './TUtoCU/annotations/'
	output_file_name = data['raw_file']
	output_file_name = output_file_name.split('/')
	output_file_name =  output_file_name[-2]
	output_pathname += output_file_name

	output_pathname = output_pathname[:-4]
	output_pathname += '.lines.txt'
	#don't forget that it's necessary to have the control file!

	output_stream = open(output_pathname, 'w+')
	outputControlStream.write(data['raw_file'])
	outputControlStream.write('\n')
	#same size. don't output negative pairs. Otherwise go for it.
	#lets go.
	for lane in range(len(data['lanes'])):
		for point in range(len(data['lanes'][lane])):
			if(data['lanes'][lane][point] > -1):
				output_stream.write(str(data['lanes'][lane][point]))
				output_stream.write(' ')
				output_stream.write(str(data['h_samples'][point])) 
				output_stream.write(' ')
		output_stream.write('\n')

	

#read the data. Get the data. output the data. json object at a time.


