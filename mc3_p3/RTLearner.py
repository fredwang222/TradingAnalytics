import numpy as np  # http://www.numpy.org
import math
import random
from scipy import stats
'''
inf = open("wine-data/winequality-red.csv")
data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

# compute how much of the data is training and testing
train_rows = math.floor(0.6* data.shape[0])
test_rows = data.shape[0] - train_rows

# separate out training and testing data
trainX = data[:train_rows,0:-1]
trainY = data[:train_rows,-1]
testX = data[train_rows:,0:-1]
testY = data[train_rows:,-1]
'''
class RTLearner:
	def __init__(self,leaf_size,verbose = False):
		self.leaf_size = leaf_size
		self.verbose = verbose
		
	def isSame(self,dataY):
		#print dataY.shape
		it = dataY.shape[0]
		tmp = dataY[0]
		for i in range (0,it):
			if(tmp != dataY[i]):
				return False
		#print "XXXX"
		return True	

	'''
	Split data function
	'''

	def splitdata(self,dataX,dataY,featureid,splvalue):
		idleft = []
		idright = []
		for i in range(0,dataX.shape[0]):
			if dataX[i][featureid]<=splvalue:
				idleft.append(i)
			else:
				idright.append(i)
		dataXleft = dataX[idleft]
		dataYleft = dataY[idleft]
		dataXright = dataX[idright]
		dataYright = dataY[idright]
		return dataXleft,dataYleft,dataXright,dataYright

	'''
	The feture generator
	'''
	def rdfea(self,data):
		numoffea = data.shape[1]
		tmp = random.randint(0,numoffea-1)
		return tmp

	'''
	The split value generator
	'''
	def rdsplv(self,data):
		numofrows = data.shape[0]
		if numofrows == 2:
			tmp1 = 0
			tmp2 = 1
		else:
			tmp1 = random.randint(0,numofrows/2)
			tmp2 = random.randint(numofrows/2,numofrows-1)

		rs = []
		#print "Datashape",data.shape
		for i in range (0,data.shape[1]):
			#print rs
			rs.append((data[tmp1][i]+data[tmp2][i])/2)
			#print "NEW",rs
		return rs,data[tmp1]

	'''
	This is buildtree function
	'''
	def buildtree(self,dataX,dataY):
		if dataX.shape[0] <= self.leaf_size:
			m = stats.mode(dataY)[0].tolist()[0]
			return np.array([[-1,m,None,None]])
													  #-1 means 'leaf'
		#print "buildtreedataY", dataY.shape,dataX.shape
		if self.isSame(dataY) == True:
			return np.array([[-1,dataY.mean(),None,None]])
		

		rdfeaid = self.rdfea(dataX)
		splvaluelist,tempcheck = self.rdsplv(dataX)

		#print splvaluelist
		#print rdfeaid
		#print splvaluelist[rdfeaid]
		splitvalue = splvaluelist[rdfeaid]
		while splitvalue == tempcheck[rdfeaid]:
			rdfeaid = self.rdfea(dataX)
			splvaluelist,tempcheck = self.rdsplv(dataX)
			splitvalue = splvaluelist[rdfeaid]

		dataXleft,dataYleft,dataXright,dataYright = self.splitdata(dataX,dataY,rdfeaid,splitvalue)
		#print "Line86"
		
		if dataXleft.shape[0]==0:
			print "LEFT EMPT"
			m = stats.mode(dataY)[0].tolist()[0]
			return np.array([[-1,m,None,None]])
		if dataXright.shape[0]==0:
			print "RIGHT EMPT"
			#print dataY
			#print rdfeaid
			#print splvaluelist

			m = stats.mode(dataY)[0].tolist()[0]
			return np.array([[-1,m,None,None]])
		

		lefttree = self.buildtree(dataXleft,dataYleft)
		righttree = self.buildtree(dataXright,dataYright)
		#print "LFT TREE is",lefttree
		
		root = np.array([[rdfeaid,splitvalue,1,lefttree.shape[0]+1]])
		return np.concatenate((root,np.concatenate((lefttree,righttree),axis=0)),axis=0)


	def addEvidence(self,dataX,dataY):
		self.TrainX = dataX
		self.TrainY = dataY
		self.nofrows = dataX.shape[0]
		self.nofcols = dataX.shape[1]
		
		self.Tree = self.buildtree(dataX,dataY)
		return self.Tree
		#print self.Tree
		#print self.Tree.shape
		#print self.Tree[0][1]
	
	def singlequery(self,onePieceOfData):
		tree = self.Tree
		i = 0
		currentrow = tree[i]
		while currentrow[0] != -1:
			sptf = currentrow[0]
			splv = currentrow[1]
			if onePieceOfData[sptf]<=splv:
				tmp = currentrow[2]
				i+=tmp
			else:
				tmp = currentrow[3]
				i+=tmp
			currentrow = tree[i]
		#print i
		#print tree[i]
		return tree[i][1]

	def query(self,testX):
		rs = []
		for i in range (0,testX.shape[0]):
			rs.append(self.singlequery(testX[i]))
		ret = np.array(rs)
		return ret
		
			
			
		





		
		



#LE = RTLearner(1,False)
#LE.addEvidence(trainX,trainY)
#LE.query(trainX)

