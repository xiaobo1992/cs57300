import numpy as np
import dataprocessing as a
import spheric_means as smeans
import cluster
from sklearn.cluster import KMeans
import cross_validation as cross	
import random

def penalty(k):
	return  k

def combine(x,y):
	new = list()
	for key,item in enumerate(x):
		f1 = item[:-1]
		f2 = y[key]
		new.append(f1+f2)
	return new
	
	
def score(Wp, Wnp): 
	for k in [10,20,50,100,200]:
		print "k = {0}".format(k)
		print "Kmeans: "
		kmeans_p = KMeans(init='k-means++', n_clusters= k,precompute_distances= True)
		kmeans_np = KMeans(init='k-means++', n_clusters= k,precompute_distances= True)
		score_p = kmeans_p.fit(Wp)
		score_np = kmeans_np.fit(Wnp)
		
		
		print "Wp cluster score: {0}".format(score_p.inertia_ + penalty(k))
		print "Wnp cluster score: {0}".format(score_np.inertia_ + penalty(k))
		
		print "Spheric means"
		mu,clusters = smeans.find_centers(Wp,k);
		print "Wp cluster score: {0}".format(smeans.score(clusters,mu) - penalty(k))
		mu,clusters = smeans.find_centers(Wnp,k);
		print "Wnp cluster score: {0}".format(smeans.score(clusters,mu) - penalty(k))
		
		
def test1(matrix_pos,matrix_neg):
	#get score from both matrix
	score(matrix_pos,matrix_neg)
	
def test2(kmeans_feature,smeans_feature):
		
	print "Approach A (Kmeans):"
	cross.crossValidation(kmeans_feature)
	print "Approach B (Spheric means):"
	cross.crossValidation(smeans_feature)
	
def test3(origin_feature,kmeans_feature):
	
	print "Approach A (Origin Feature):"
	cross.crossValidation(origin_feature)	
	print "Apporach B (kmans):"		
	cross.crossValidation(kmeans_feature)
	
def test4(origin_feature,kmeans_feature,combine_feature):

	print "Approach A (Origin Feature):"
	cross.crossValidation(origin_feature)	
	print "Apporach B (kmans):"		
	cross.crossValidation(kmeans_feature)
	print "Aapproach C (combine):"
	cross.crossValidation(combine_feature)
	
def main():
	
	filename = "stars_data.csv"
	data = a.read_data(filename)
	data.pop(0)
	random.shuffle(data)
	frequency = a.frequency_word(data)
	
	data_neg = [x for x in data if int(x[6]) == 1]
	data_pos = [x for x in data if int(x[6]) == 5]

	matrix_pos = np.zeros((2000,2500))
	matrix_neg = np.zeros((2000,2500))
	matrix_pos = cluster.create_matrix(matrix_pos,data_pos,frequency)
	matrix_neg = cluster.create_matrix(matrix_neg,data_neg,frequency)
	
	kmeans_feature = cluster.kmeans_bin(data,matrix_pos,matrix_neg,frequency,50)
	smeans_feature = cluster.smeans_bin(data,matrix_pos,matrix_neg,frequency,50)	
	origin_feature = a.create_binary_feature(data,frequency,6)
	
	sample_origin_feature = a.create_binary_feature(data,random.sample(frequency,100),6)
	combine_feature = combine(kmeans_feature,sample_origin_feature)
	
	print "Test1"
	test1(matrix_pos,matrix_neg)
	print "Test2"
	test2(kmeans_feature,smeans_feature)
	print "Test3"
	test3(origin_feature,kmeans_feature)
	print "Test4"
	test4(sample_origin_feature,kmeans_feature,combine_feature)
		
if __name__ == "__main__":
    main()		