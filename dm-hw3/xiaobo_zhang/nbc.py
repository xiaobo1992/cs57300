import dataprocessing as a
import sys
	
def main(args):		
	#take argument
	trainfile = args[1]
	testfile = args[2]
	classlabel = int(args[3])
	printWord = int(args[4])
		
	
	#set train file an dtest file
	train = a.read_data(trainfile)
	test  = a.read_data(testfile)
	
	#get top 2000 frequency
	fre = a.frequency(train)
	
	
	#if yes, print Words
	if (printWord == 1):
		a.printTopwords(fre)
	
	#create binary feature for boss data
	train = a.create_binary_feature(train,fre,classlabel)
	test = a.create_binary_feature(test,fre,classlabel)
	
	#get probability table based on train data
	prob_table,pYes,pNo = a.train_nbc(train)
	
	#use probability table for testing,and return result
	result = a.test_nbc(prob_table,test,pYes,pNo)
	
	#get test class label
	classlabel = [x[-1] for x in test]
	
	
	#use zero one difference figure out result
	diff = a.zero_onr_loss(result,classlabel)
	
	print "ZERO-ONE-LOSS {0}".format(diff)

if __name__ == "__main__":
    main(sys.argv)


		