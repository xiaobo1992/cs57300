import csv
import string
import random

def write_file(filename,n):
	data = read_data(filename)
	data.pop(0)
	sample,test = sampling(data,n);
	
	with open('train-set.dat', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(sample)
	with open('test-set.dat', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(test)
		
#read data from csv file
def read_data(filename):
	data = []
	#read file line by line and store into the array
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			data.append(row);
	#remove header from data
	return data

#sampling data 
def sampling(data,n):
	#choose random sample n
	sample_data = random.sample(data,n)
	#rest of them store in test set
	test_data = [x for x in data if x not in sample_data]
	return sample_data,test_data
	
#get word frequency of dataset
def frequency_word(data):
	#declare word frequency dictionary
	word_frequency = dict()
	table = string.maketrans("","")
	
	#counting frequency
	for row in data:
		#take the sentence
		sentence =  row[7]
		#remove the punctuation from sentence
		sentence = sentence.translate(table,string.punctuation)
		#split word into array
		sentence = sentence.split()	
		
		for word in sentence:
			#lower case the word
			word = word.lower()
			#if the word already in frequency table
			if (word in word_frequency):
				word_frequency[word] += 1
			#if not, add new key
			else:
				word_frequency[word] = 1

	#sorted the frequency by value		
	word_frequency = sorted(word_frequency,reverse=True,key = word_frequency.get)
	#take 201 to 2200 attributes for analysing
	result = [word_frequency[i] for i in range(101,2101)]
	return result;

def printTopwords(word_frequency):
	for i in range(10):
		print "WORD{0} {1}".format(i,word_frequency[i])
		
#create binary feature
def create_binary_feature(sample,frequency,classlabel):
	bin = list();
	for row in sample:
		#get text
		text = row[7];
		#strip punctuation
		text = text.translate(string.maketrans("",""),string.punctuation)
		#split text
		text = text.split()

		#initialize a feature list
		feature = list()
		#construct binary feature for each word 
		for word in frequency:
			#if word appear
			if (word in text):
				feature.append(1)
			#if word not appear
			else:
				feature.append(0)
		
		#add class label at back
		
		#isFuny binary feature
		if (classlabel == 5):
			score = int(row[4])
			#define binary class
			if (score == 0):
				feature.append(0)
				feature.append(1)
			else:
				feature.append(1)
				feature.append(0)
		#isPositive binary feature
		else:
			score = int(row[6])
			if (score == 5):
				feature.append(1)
				feature.append(0)
			else:
				feature.append(0)
				feature.append(1)
		#append to whole data
		bin.append(feature)
	return bin

#smooth function
def smooth(c,label):
	return float(c+1)/(label + 2)

#take probability
def probablity(c,label):
	prob = float(c)/label
	#if probability is 0, smooth it
	if(prob == 0):
		prob = smooth(c,label)
	return prob	

#give binary feature to calculate probability table
def train_nbc(data):
	#get class label, # of yes label, and #of no label
	label = [x[-1] for x in data]
	yes =  label.count(1)
	no =  label.count(0)
	
	#get class label result
	pYes = float(yes)/(yes+no)
	pNo = float(no)/(yes+no)
	
	#get list
	train = list()

	for i in range(len(data[1]) - 1):
		attribute = [[x[i],x[-1]] for x in data]
		#count occurrence
		c00 = attribute.count([0,0])	
		c01 = attribute.count([0,1])	
		c10 = attribute.count([1,0])	
		c11 = attribute.count([1,1])	
				
		#count probability
		p00 = probablity(c00,no)
		p01 = probablity(c01,yes)
		p10 = probablity(c10,no)
		p11 = probablity(c11,yes)  
		
		train.append([p00,p01,p10,p11])
	
	return train,pYes,pNo	
	
def test_nbc(train,test,pY,pN):
	result =list()
	#calculate probability
	for row in test:
		pYes = 1
		pNo = 1
		for i in range(len(row) -1):
			if (row[i] == 0 ):
				pYes *= train[i][1]	
				pNo *= train[i][0]
			else:
				pYes *= train[i][3] 
				pNo *= train[i][2]
		
		pYes *= pY
		pNo *= pN
		
		#decide class label
		if pYes >= pNo:
			result.append(1)
		else:
			result.append(0)
	return result;

	
def zero_one_loss(result,label):
	diff = 0
	#get difference
	for i in range(len(result)):
		if (result[i] != label[i]):
			diff += 1
	return float(diff)/len(result)