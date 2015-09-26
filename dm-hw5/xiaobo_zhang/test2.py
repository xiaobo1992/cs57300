import numpy as np
import dataprocessing as a	
import random
import itertools
import operator
import scipy.stats
import math

def construct(data,words):
	newdata = []
	for d in data:
		temp = []
		for index, value in enumerate(d):
			if value == 1:
				temp.append(words[index])
		newdata.append(temp)
	return newdata
	
def setWords(words):
	new = []
	for word in words:
		new.append([word])
	return map(frozenset,new)
	
def simple_count(D,canditate):
	count = 0 
	for data in D:
		if canditate.issubset(data):
			count += 1
	return count

def chisquare(x):
	observed = x
	total = sum(x)
	expected = []
	
	expected.append((observed[0] + observed[1]) * (observed[0] + observed[2])/float(total))
	expected.append((observed[1] + observed[0]) * (observed[1] + observed[3])/float(total))
	expected.append((observed[2] + observed[3]) * (observed[2] + observed[0])/float(total))
	expected.append((observed[3] + observed[2]) * (observed[1] + observed[3])/float(total))
	
	conf = 0
	for i in range(4):
		conf += math.pow(observed[i]-expected[i],2)/expected[i]
	
	return conf
	
def q2(D,object):
	result = []
	
	f = open('rules','w')
	a = object[0]
	b = object[1]
	c = object[2]
	d = object[3]
	
	#generalize rules
	antecedant = a
	subsequent = b
	
	A = simple_count(D,antecedant)  #friendly
	B = simple_count(D,subsequent)	#isPositive
	C = simple_count(D,antecedant | subsequent) #friendly & isPositive
	contigency = []
					
	contigency.append(C)
	contigency.append(B - C) 
	contigency.append(A - C)
	contigency.append(5000 - (A + B- C))
		
	score = chisquare(contigency)
	accuracy = (contigency[0]+ contigency[3])/float(5000)
	writeRules(f,contigency,antecedant,subsequent,score,accuracy)
		
	#rule 2
	antecedant = a | c 
	subsequent = b
	
	A = simple_count(D,antecedant)  #friendly
	B = simple_count(D,subsequent)	#isPositive
	C = simple_count(D,antecedant | subsequent) #friendly & isPositive
	
	contigency = []					
	contigency.append(C)
	contigency.append(B - C) 
	contigency.append(A - C)
	contigency.append(5000 - (A + B- C))
		
	score = chisquare(contigency)
	accuracy = (contigency[0]+ contigency[3])/float(5000)
	writeRules(f,contigency,antecedant,subsequent,score,accuracy)
	#rule 3
	antecedant = a | c | d
	subsequent = b
	
	A = simple_count(D,antecedant)  #friendly
	B = simple_count(D,subsequent)	#isPositive
	C = simple_count(D,antecedant | subsequent) #friendly & isPositive
	
	contigency = []					
	contigency.append(C)
	contigency.append(B - C) 
	contigency.append(A - C)
	contigency.append(5000 - (A + B- C))
		
	score = chisquare(contigency)
	accuracy = (contigency[0]+ contigency[3])/float(5000)
	writeRules(f,contigency,antecedant,subsequent,score,accuracy)

def writeRules(f,contigency,antecedant,subsequent,score,accuracy):	
	f.write("Rule: " + str(antecedant) + "->" + str(subsequent)+'\n'),
	f.write("                        "+ str(antecedant) + "|   not   " + str(antecedant)+ '\n')
	f.write(str(subsequent)+ "           " + str(contigency[0]) + "      " + str(contigency[1])+ '\n')
	f.write("not " + str(subsequent)+ "      " + str(contigency[2]) + "          " + str(contigency[3]) + '\n')
	f.write("score: "  + str(score) + '\n')
	f.write("accuracy: " + str(accuracy) + '\n\n\n')
	
def main():
	
	#data preprocessing
	filename = "stars_data.csv"
	data = a.read_data(filename)
	data.pop(0)
	random.shuffle(data)
	words = a.frequency_word(data)	
	features = a.create_binary_feature(data,words,6)
	words.append("isPositive")
	words.append("isNegative")
	minsupport = 0.03
	minconf = 0.25
	
	D = construct(features,words)
	D = map(set, D)
	t = []
	t.append(frozenset(['friendly']))
	t.append(frozenset(['isPositive']))
	t.append(frozenset(['staff']))
	t.append(frozenset(['favorite']))
	
	q2(D,t)
	'''
	for i in range(30):
		# print rulesObject[i].antecedant
		# print rulesObject[i].subsequent
		print rulesObject[i].confi
	'''
if __name__ == "__main__":
    main()