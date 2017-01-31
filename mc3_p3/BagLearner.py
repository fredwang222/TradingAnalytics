import RTLearner as rt
import numpy as np
from scipy import stats
import math
import random
'''
inf = open("wine-data/winequality-red.csv")
data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

# compute how much of the data is training and testing
train_rows = math.floor(0.6* data.shape[0])
test_rows = data.shape[0] - train_rows

# separate out training and testing data
trainX = data[:train_rows,0:-1]
trainY = data[:train_rows,-1]
gltestX = data[train_rows:,0:-1]
gltestY = data[train_rows:,-1]

'''



class BagLearner:
	def __init__(self,learner = rt.RTLearner, kwargs = {"leaf_size":5,"verbose":False}, bags = 20, boost = False, verbose = False):
		self.bags = bags
		self.verbose = verbose
		self.boost = boost
		self.kwargs = kwargs
		self.learnerlist = []
		for i in range(0,bags):
			self.learnerlist.append(learner(**kwargs))
		
	def addEvidence(self,XTrain,YTrain):
		self.baglist = []
		for i in range(0,self.bags):
			self.baglist.append(self.learnerlist[i].addEvidence(XTrain,YTrain)) #To make every RTLearner object in learner list generate their own tree
		#print self.learnerlist[5].Tree
		#print self.baglist[5]

	def query(self,TestX):
		self.rstcombo = []
		for i in range (0,self.bags):
			tmp = self.learnerlist[i].query(TestX)
			self.rstcombo.append(tmp)
		totalrsmetrix = np.array(self.rstcombo)
		ret = []
		for i in range (0,totalrsmetrix.shape[1]):
			tmp = totalrsmetrix[:,i]
			m = stats.mode(tmp)[0].tolist()[0]
			ret.append(m)

		rs = np.array(ret)
		return rs

		#m = stats.mode(totalrsmetrix[:,5])
		#print type(m[0])
		










'''
bg = BagLearner(rt.RTLearner,{"leaf_size":1},200,False,False)
bg.addEvidence(trainX,trainY)
rs = bg.query(trainX)
print rs

'''


