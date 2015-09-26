import dataprocessing as a
import numpy
#a.write_file("stars_data.csv",3500)

for file in ["funny_data.csv","stars_data.csv"]:
	data = a.read_data(file)
	data.pop(0)
	
	#define class label
	if (file == "stars_data.csv"):
		classlabel = 7
	elif (file == "funny_data.csv"):
		classlabel = 5
	
	print "Data File: {0}".format(file)
	
	totalloss = list()
	for size in [0.1,0.5,0.9]:
		samplesize = int(5000 * size)
		print "Train size: {0}".format(samplesize)
		
		loss = list()
		base = list()
		for i in range(10):
			#sampling data
			train,test = a.sampling(data,samplesize)
			
			#get top 2000 frequency
			fre = a.frequency(train)
			
			#create binary feature for boss data
			
			train = a.create_binary_feature(train,fre,classlabel)
			test = a.create_binary_feature(test,fre,classlabel)
				
			#get probability table based on train data
			prob_table,pYes,pNo = a.train_nbc(train)
			
			#use probability table for testing,and return result
			result = a.test_nbc(prob_table,test,pYes,pNo)
			
			#get test class label
			label = [x[-1] for x in test]
			
			#use zero one difference figure out result
			diff = a.zero_onr_loss(result,label)
			loss.append(diff)
			
			#baseline default error
			if pYes >= pNo:
				label = [1 for i in range(len(test))]
			else:
				label = [0 for i in range(len(test))]
			
			diff = a.zero_onr_loss(result,label)
			base.append(diff)
			
		print "ZERO-ONE-LOSS: {0}".format(loss)
		print "Mean: {0}".format(numpy.mean(loss))
		print "stdev {0}".format(numpy.std(loss))
		print "Baseline error"
		print "Mean: {0}".format(numpy.mean(base))
		print "stdev {0}".format(numpy.std(base))
		totalloss.append(loss)
	print totalloss;