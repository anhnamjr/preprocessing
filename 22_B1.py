import pandas as pd
import numpy as np 
from math import *
import sys

def minArr(Array):
	minElement = Array[0]
	for value in Array:
		if value <= minElement:
			minElement = value

	return minElement

def maxArr(Array):
	maxElement = Array[0]
	for value in Array:
		if value >= maxElement:
			maxElement = value

	return maxElement

def minMaxNormalization(dataframe, Label):
	arr = dataframe[Label].values
	length = arr.shape[0]
	minElement = minArr(arr)
	maxElement = maxArr(arr)
	newMax = 1
	newMin = 0
	for i in range(0, length):
		IdScale = ((arr[i] - minElement) / (maxElement - minElement))*(newMax - newMin) + newMin 
		dataframe.loc[i,Label] = IdScale
	
	return dataframe

def meanArray(Array):
	s = 0
	for value in Array:
		s += value;
	return s/len(Array)

def zScoreNormalization(dataframe, Label):
	arr = dataframe[Label].values
	length = arr.shape[0]
	s = 0
	variance = 0
	mean = np.mean(arr)

	for value in arr:
		variance += (value - mean)**2

	#stadard deviation
	stdv = sqrt(variance/(length - 1))
	for i in range(0, length):
		IdScale = (arr[i] - mean) / stdv
		dataframe.loc[i,Label] = IdScale
	return dataframe

def binningByEqualWidth(dataframe, Bin, Label):
	arr = dataframe[Label].values
	minElement = minArr(arr)
	maxElement = maxArr(arr)

	#find the width
	w = (maxElement - minElement) / Bin
	if w - int(w) > 0.5:
		w = int(w) + 1
	else:
		w = int(w)

	#Find the value domain
	binArri = []
	for i in range(0, Bin + 1):
		binArri += [minElement + i * w]

	#start binning
	binArr = []
	for i in range(0, Bin):
		Temp = []
		for j in arr:
			if j >= binArri[i] and j < binArri[i+1]:
				Temp += [j]
		binArr += [Temp]

	#Find the mean of each Bin
	meanTemp = []
	for i in range(0, Bin):
		meanTemp += [meanArray(binArr[i])]

	#replace each data with the corresponding mean
	res = []
	for value in arr:
		for i in range(0, Bin):
			if value >= binArri[i] and value < binArri[i+1]:
				res += [meanTemp[i]]
		if value >= binArri[Bin]:
			res += [value]
	for i in range(0, len(res)):
		dataframe.loc[i,Label] = res[i]

	return dataframe

def binningByEqualFrequency(dataframe, Bin, Label):
	arr = dataframe[Label].values
	length = arr.shape[0]

	#find the len of bin
	n = length/Bin
	if n - int(n) > 0.5:
		n = int(n) + 1
	else:
		n = int(n)

	#sort array
	sortArr = np.sort(arr)
	
	#start binning
	binArr = []
	for i in range(0, Bin):
		temp = []
		for j in range(i * n, (i + 1) * n):
			if j >= length:
				break
			temp += [sortArr[j]]
		if len(temp) != 0: 
			binArr += [temp]

	length2 = 0
	for i in range(0, Bin):
		length2 += len(binArr[i])

	#case: length2 > length: Put all remaining values ​​in the last Bin
	if length2 < length:
		for i in range(length2, length):
			binArr[Bin - 1] += [sortArr[i]]

	#Find the mean of each bin
	meanTemp = []
	for i in range(0, Bin):
		meanTemp += [meanArray(binArr[i])]

	#replace each data with the corresponding mean
	res = []	
	for value in arr:
		for i in range(0, Bin):
			if value in binArr[i]:
				res += [meanTemp[i]]
				break

	for i in range(0, len(res)):
		dataframe.loc[i,Label] = res[i]

	return dataframe

def deleteMissingValues(dataframe, Label):
	bool_df = dataframe[Label].isnull()
	length = dataframe.shape[0]

	#Find the value NaN and delete that row
	for i in range(0, length):
		if bool_df[i] == True:
			dataframe = dataframe.drop([i], axis=0)

	return dataframe

def handleMissingValues(dataframe, Label):
	bool_df = dataframe[Label].isnull()
	length = dataframe.shape[0]

	#find the mean of column Label
	Mean = dataframe[Label].mean()

	#replace value NaN by the Mean corresponding
	for i in range(0, length):
		if bool_df[i] == True:
			dataframe.loc[i, Label] = Mean

	return dataframe



def main():
	ListCommand = (sys.argv)
	csvIn = './' + ListCommand[1]
	csvOut = './' + ListCommand[2]
	dataframe = pd.read_csv(csvIn, header=0)
#print(dataframe)
	task = ListCommand[3]
	if task == 'a':
		Label = []
		for i in range(4, len(ListCommand)):
			Label += [ListCommand[i]]
		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = minMaxNormalization(newDF, Label[i])
	elif task == 'b':
		Label = []
		for i in range(4, len(ListCommand)):
			Label += [ListCommand[i]]
		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = zScoreNormalization(newDF, Label[i])
	elif task == 'c':
		Bin = int(ListCommand[4])
		Label = []
		for i in range(5, len(ListCommand)):
			Label += [ListCommand[i]]

		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = handleMissingValues(newDF, Label[i])
			newDF = binningByEqualWidth(newDF, Bin, Label[i])
	elif task == 'd':
		Bin = int(ListCommand[4])
		Label = []
		for i in range(5, len(ListCommand)):
			Label += [ListCommand[i]]

		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = handleMissingValues(newDF, Label[i])
			newDF = binningByEqualFrequency(newDF, Bin, Label[i])
	elif task == 'e':
		Label = []
		for i in range(4, len(ListCommand)):
			Label += [ListCommand[i]]

		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = deleteMissingValues(newDF, Label[i])
	elif task == 'f':
		Label = []
		for i in range(4, len(ListCommand)):
			Label += [ListCommand[i]]

		newDF = dataframe
		for i in range(0, len(Label)):
			newDF = handleMissingValues(newDF, Label[i])

	newDF.to_csv(csvOut, index = None)

if __name__ == '__main__':
	main()





	
