import numpy as np
from scipy.stats import pearsonr,spearmanr
import pandas as pd
from pandas.api.types import is_numeric_dtype
def add(a, b):
	if(isinstance(a, int) or isinstance(a, float)):
		if(isinstance(b, int) or isinstance(b, float)):
			return a + b
		else:
			return str(a) + str(b)

	if(isinstance(a, list) and isinstance(b, list)):
		return a + b
	if(isinstance(a, str) and isinstance(b, str)):
		return a + b
	elif(isinstance(a, list) or isinstance(a, str)):
		return str(a) + str(b)
	else:
		print("Error!")
		return None

def calcMyGrade(assScore, midScore, pracScore, weights):
	avg = 0
	tempSum = 0

	for i in assScore:
		tempSum = tempSum + i
	avg = avg + ((tempSum/len(assScore))*weights[0])/100

	tempSum = 0
	for i in midScore:
		tempSum = tempSum + i
	avg = avg + ((tempSum/len(midScore))*weights[1])/100

	tempSum = 0
	for i in pracScore:
		tempSum = tempSum + i
	avg = avg + ((tempSum/len(pracScore))*weights[2])/100

	return avg	


class Node():
	parent = None
	leftChild = None
	rightChild = None
	key = None
	value = None

	def __init__(self, key: int, value):
		self.key = key
		self.value = value
		


	def getChildren(self):
		return [self.leftChild, self.rightChild]
	def getKey(self):
		return self.key

class Queue():
	def __init__(self):
		self.queue = []

	def push(self, val):
		self.queue.append(val)

	def pop(self):
		self.queue.pop()
	
	def checkSize(self):
		return len(self.queue)


def generateMatrix(numRows, numColumns, maxVal, minVal):
	np.random.seed(0)

	return np.random.uniform(low=minVal, high=maxVal, size=(numRows, numColumns))
	# myArray = np.zeros(shape(numRows, numColumns))

	# for i in len(myArray):
	# 	for j in len(myArray[0]):
	# 		myArray[i][j] = 

def multiplyMat(matrixA, matrixB):
	try: 
		newMatrix = np.matmul(matrixA, matrixB)
	except ValueError:
		print("Incompatible Matrices")
		return None

	return newMatrix

def statsTuple(a, b):
	sum_a = np.sum(a)
	sum_b = np.sum(b)
	mean_a = np.mean(a)
	mean_b = np.mean(b)
	min_a = np.amin(a)
	min_b = np.amin(b)
	max_a = np.amax(a)
	max_b = np.amax(b)
	(r, pearson) = pearsonr(a,b)
	(rho, spearman) = spearmanr(a,b)

	return (sum_a, mean_a, min_a, max_a, sum_b, mean_b, min_b, max_b, r, rho)

# def pandas_func(file):
# 	# filedata = pd.read_csv(file)
# 	filedata = pd.read_csv("../Desktop/ExampleTab.txt", delim_whitespace=True)
# 	listOfMeans = []
# 	listOfColumnNames = []
	
# 	columns = filedata.columns.values.tolist()
# 	for i in columns:
# 		if(np.issubdtype(filedata[i].dtype, np.number)):
# 			listOfMeans.append(filedata[i].mean())
# 		else:
# 			listOfColumnNames.append(i)

# 	return listOfMeans, listOfColumnNames


def pandas_func(file_name):
	filedata = pd.read_csv(file_name, sep='\t')
	ListOfMeans = list()
	ListOfColumnNames = list()
	columns = filedata.columns.values.tolist()
	for i in columns:
		if(filedata[i].dtype.kind in 'biufc'):
			ListOfMeans.append(round(filedata[i].mean(),2))
		else:
			ListOfColumnNames.append(i)
	return ListOfMeans, ListOfColumnNames

def main():
	print(pandas_func("ExampleTab.txt"))
	# myClass = Node(2, 36)
	# print(myClass.getKey())
	# print(myClass.getChildren())
	





if __name__ == '__main__':
	main()