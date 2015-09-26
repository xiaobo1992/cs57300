import dataprocessing as a
import spheric_means as smeans
import numpy as np
import string
from sklearn.cluster import KMeans

def create_matrix(matrix, data, frequency):
	for i in range(len(data)):
		#get text
		text =	data[i][7]
		#strip punctuation
		text = text.translate(string.maketrans("",""),string.punctuation)
		#split text
		text = text.split()
		
		#count frequency
		for word in text:
			if (word in frequency):
				j = frequency.index(word)
				matrix[j][i] += 1
	return matrix
	
def clusetering_world(matrix,k):
	kmeans = KMeans(init='k-means++', n_clusters= k,precompute_distances= True)
	result = kmeans.fit_predict(matrix)
	return result
	
def create_topic_feature(result, frequency):
	topic_features = list()
	for i in range(50):
		group = [x for x,y in enumerate(result) if y == i]
		feature = list()
		#adding words to cluster
		for j in group:
			feature.append(frequency[j])
		topic_features.append(feature)
	return topic_features
	
def create_binary_review_feature(data,topic_features,classlabel):
	bin_feature = list()
	for text in data:
		
		review = text[7]	
		#strip punctuation
		review = review.translate(string.maketrans("",""),string.punctuation)
		#split text
		review = review.split()
		
		feature = [0 for i in range(100)]
		for i in range(len(topic_features)):
			for word in review:
				if (word in topic_features[i]):
					feature[i] = 1
					break
		
		if int(text[classlabel]) == 1:
			feature.append(1)
		else:
			feature.append(0)
			
		bin_feature.append(feature)
	return bin_feature

def label(matrix,clusters):

	result = list()
	for row in matrix:
		for key, cluster in clusters.items():
			if in_cluster(row,cluster):
				result.append(key)
				break
	return result
	
def in_cluster(row, cluster):
	for item in cluster:
		if np.array_equal(row,item):
			return True
	return False
	
	
def kmeans_bin(data,matrix_pos,matrix_neg,frequency,k):

	#define k means
	clusters_pos = clusetering_world(matrix_pos,k)
	clusters_neg = clusetering_world(matrix_neg,k)
	
	topic_pos = create_topic_feature(clusters_pos,frequency)
	topic_neg = create_topic_feature(clusters_neg,frequency)
	
	topic = topic_pos + topic_neg
	result = create_binary_review_feature(data,topic,6)	
	
	with open('kmeans_word.txt', 'w') as f:
		for t in topic:			
			f.write(str(t))
			f.write('\n')		
	return result

def smeans_bin(data,matrix_pos,matrix_neg,frequency,k):
	
	
	center_pos, cluster_pos = smeans.find_centers(matrix_pos,k)
	center_neg, cluster_neg = smeans.find_centers(matrix_neg,k)

	clusters_pos = label(matrix_pos, cluster_pos)
	clusters_neg = label(matrix_neg, cluster_neg)
		
	topic_pos = create_topic_feature(clusters_pos,frequency)
	topic_neg = create_topic_feature(clusters_neg,frequency)
	
	topic = topic_pos + topic_neg
	with open('smeans_word.txt', 'w') as f:
		for t in topic:			
			f.write(str(t))
			f.write('\n')
	result = create_binary_review_feature(data,topic,6)	
	
	return result
