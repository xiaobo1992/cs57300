import Apriori as ampriori
import operator
import dataprocessing as a	
import random
 
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
	
	L,support_count = ampriori.frequentItemsetGeneration(features,words,minsupport)
	print len(L[0]) + len(L[1]) + len(L[2])
	
	rules,r = ampriori.ruleGeneration(L,support_count,minconf)
	print len(rules)
	
	rules = sorted(rules.items(),key=operator.itemgetter(1),reverse= True)
	rules = [rules[i] for i in range(30)]
	for index, rule in enumerate(rules):
		print rule
	
if __name__ == "__main__":
    main()		