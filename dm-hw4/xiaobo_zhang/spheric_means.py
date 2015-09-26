import numpy as np
import random
from sklearn.cluster import KMeans

def cluster_points(X,mu):
	clusters = {}

	#calculate best points
	for x in X:
		
		bestmukey = max([(i[0], consine_similarity(x,mu[i[0]])) \
                    for i in enumerate(mu)], key = lambda t:t[1])[0]
		
		try:
			clusters[bestmukey].append(x)
		except KeyError:
			clusters[bestmukey] = [x]
	return clusters

def normalize(data):
	for index, x in enumerate(data):
		norm = np.linalg.norm(x)
		#if all vector is zero, switch to one and redo the norm
		
		if norm == 0:
			x = [1 for i in x]
			norm = np.linalg.norm(x)	
			data[index] = x / norm
		else:
			data[index] /= norm		
	return data
	
def reevaluate_centers(mu,clusters):
	newmu = []
	keys = sorted(clusters.keys())
	for k in keys:
		sum = np.sum(clusters[k],axis = 0)
		norm = np.linalg.norm(sum)		
		newmu.append(sum / norm)	
	return newmu
		
def has_converged(mu,oldmu):
	return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
		
def find_centers(X,K):
	normalize(X)
	oldmu = random.sample(X,K)
	mu = random.sample(X,K)
	
	while not has_converged(mu, oldmu):
		oldmu = mu
		clusters = cluster_points(X,mu)
		mu = reevaluate_centers(mu,clusters)
	return (mu,clusters)

def score(clusters,mu):
	score = 0
	for index, center in enumerate(mu):
		for item in clusters[index]:
			score += consine_similarity(center,item)
	return score

def consine_similarity(x,y):
	return np.dot(x,y)/ (np.linalg.norm(x) * np.linalg.norm(y))
