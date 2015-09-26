import random
import dataprocessing as nbc
import numpy 
import math

def crossValidation(data):
	
	X = kfold(data,10)
	for tss in [100,250,500,1000,2000]:
		print "tss = ",tss
		loss = list()
		for i in range(10):
			test_set = X[i]
			#take rest of data
			train_data = list()
			for j in range(10):
				if j != i:
					train_data += X[j]
			train_set = random.sample(train_data,tss)
			train, pYes, pNo = nbc.train_nbc(train_set)
			result = nbc.test_nbc(train, test_set,pYes,pNo)
			label = [x[-1] for x in test_set]
			diff = nbc.zero_one_loss(result, label)
			
			loss.append(diff)
		print loss
		print "mean: ",numpy.mean(loss)
		print "std error: ",standard_error(loss,10)
		
			
def kfold(X, n):
	
	total = len(X)
	period = total / n
	data = list()
	for i in range(n):
		begin = i * period;
		data.append(X[begin : begin + period])		
	return data

def standard_error(x,n):
	return numpy.std(x)/math.sqrt(n)
	