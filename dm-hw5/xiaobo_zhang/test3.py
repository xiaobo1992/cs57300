import numpy as np
import dataprocessing as a	
import random
import itertools
import operator
import scipy.stats
import math
import pickle
import Apriori as apriori
 
def ruleG(L,support,minconf):
	alpha = 0.05 / (609 + 200)
	rules = {}
	rulesobject = []
	for k in [2,3]:
		l = L[k-1]
		for can in l:
			subsets = set(itertools.combinations(can,k-1))			
			for subset in subsets:
				#A->B
				antecedant = frozenset(subset)		
				subsequent = can - antecedant
				
				A = support[antecedant]  #friendly
				B = support[subsequent]	#isPositive
				C = support[can] #A & B
				
				contigency = [[C,A - C],[B-C,5000 - (A+B-C)]]
				confi  = scipy.stats.chi2_contingency(contigency)
				
				if confi[1] <= alpha:
					left = str(antecedant)
					right = str(can - antecedant)
					key = left, " -> " ,right
					rules[key] = confi[0]
				
	return rules
	
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
	minconf = 3.81
	
	L,support_count = apriori.frequentItemsetGeneration(features,words,minsupport)
	print len(L[0]) + len(L[1]) + len(L[2])
	rules = ruleG(L,support_count,minconf)
	print len(rules)
	rules = sorted(rules.items(),key=operator.itemgetter(1),reverse= True)
	rules = [rules[i] for i in range(30)]
	
	for rule in rules:
		print rule
	
if __name__ == "__main__":
    main()