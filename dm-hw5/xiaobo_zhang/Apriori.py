import numpy as np
import dataprocessing as a	
import random
import itertools
import operator
import scipy.stats
import math
import pickle

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
	
def supp_count(D,canditates,minsupport):
	result = {}
	size = len(D)
	
	for data in D:
		for canditate in canditates:
			if canditate.issubset(data):
				result.setdefault(canditate,0)
				result[canditate] += 1
				
	satisfy = []			
	sup = {}
	print len(result)
	for key in result:
		support = float(result[key]) / size
		if support >= minsupport:
			satisfy.insert(0,key)
		sup[key] = result[key]
	return satisfy,sup

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
	
def ruleGeneration(L,support,minconf):
			
	h1 = L[0]
	rules = {}
	rulesobject = []
	for k in [2,3]:
		l = L[k-1]
		for can in l:
			subsets = set(itertools.combinations(can,k-1))			
			for subset in subsets:
				antecedant = frozenset(subset)		
				subsequent = can - antecedant	
				up = support[can]				
				bottom = support[antecedant]
				confi = float(up) / bottom
				#if confidence is greater than threshold
					
				if confi >= minconf:
					left = str(antecedant)
					right = str(can - antecedant)
					key = left, " -> " ,right
					#print key
					#print key," ",confi
					rules[key] = confi
					#sprint type(key)
					rulesobject.append(Rules(can,antecedant,subsequent,confi))
	
	#print len(rules)
	return rules,rulesobject			
			
def CandidateItemsetGeneration (frequentItem, minsupport,k):
	size = len(frequentItem)
	result = []
	
	#self join
	for i in range(size):
		for j in range(i + 1,size):			
			l1 = list(frequentItem[i])[:k - 2]
			l2 = list(frequentItem[j])[:k - 2]
			l1.sort()
			l2.sort()
			if l1 == l2:
				result.append(frequentItem[i] | frequentItem[j])					
	
	print "prune before: ",len(result)
	#prune
	for item in result:
		subsets = set(itertools.combinations(item,k - 1))
		# print type(subsets)
		for subset in subsets:
			if frozenset(subset) not in frequentItem:
				result.remove(item)
				break
	print "prune after: ",len(result)
	return result
		

	
def frequentItemsetGeneration(data,words,minsupport):
	L = []
	D = construct(data,words)
	D = map(set, D)
	canditates = setWords(words)
	L1, support = supp_count(D,canditates,minsupport)
	L = [L1]
	print "k = 1: "
	print "support count before: ",len(canditates)
	print "support count after: ", len(L1)
	
	
	for k in [2,3]:
		print "k = ",k
		temp = CandidateItemsetGeneration (L[k-2], minsupport,k)	
		print "support count before: ",len(temp)
		temp,result = supp_count(D,temp,minsupport)
		print "support count after: ",len(temp)
		L.append(temp)
		support.update(result)
	return L,support
	
	
class Rules(object):
    def __init__(self, can,antecedant, subsequent,confi):
		self.antecedant = antecedant
		self.subsequent = subsequent
		self.confi = confi
		self.can = can
	
	
if __name__ == "__main__":
    main()		