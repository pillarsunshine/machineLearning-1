
# -*- coding:utf-8 -*-
#/usr/bin/python

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt  

def get_distance(vector1,vector2):
    distance = np.sqrt(np.sum((vector1 - vector2)**2))
    return distance

def get_distance_Manhattan(vector1, vector2):
    distance = np.sum(np.fabs(vector1 - vector2))
    return distance

def get_distance_cosine(vector1, vector2):
    cosine_theta = float(np.dot(vector1,vector2))/(np.sqrt(np.sum(vector1 ** 2)) * np.sqrt(np.sum(vector2 ** 2)))
    distance = 1 - cosine_theta
    return distance

def get_distance_pearson(vector1,vector2):
    cov_xy = np.mean((vector1 - np.mean(vector1)) * (vector2 - np.mean(vector2)))
    std_xy = np.std(vector1) * np.std(vector2)
    pearson = cov_xy / std_xy
    distance = 1 - pearson
    return distance

def reCenter(data_result,k):
    centers = []
    nrow,ncol = data_result.shape
    for j in xrange(k):                                                                                   
        data_cluster = data_result[data_result[:,ncol-1]==j]
        center = np.mean(data_cluster,axis=0)  
        #print 'center:  ',center
        centers.append(center[0:ncol-1])
    return centers

def assign(centers,data_result,k):
    nrow,ncol = data_result.shape
    costs = 0
    for i in xrange(nrow):
        distances = []
        for j in xrange(k):
            distance = get_distance(data_result[i,0:ncol-1],centers[j])
            distances.append(distance)
        cost = min(distances)
        costs += cost     
        min_index = distances.index(cost)
        data_result[i,ncol-1] = min_index        
    return data_result,costs

def kmeans(data_result,centers,k,eplise):
    loop = 0
    costs = 0
    while (loop < iter_max):
        cost_old = costs
        data_result,costs = assign(centers,data_result,k)
        centers = reCenter(data_result,k)
        if (np.fabs(cost_old - costs) < eplise):
            return data_result,costs,centers
        print 'costs',costs
        loop += 1 
    return data_result,costs,centers

def showCluster(data_result,k,centers,init_centers):
    nrow,ncol = data_result.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    for i in xrange(nrow):  
        markIndex = int(data_result[i,ncol-1])
        plt.plot(data_result[i,0], data_result[i,1], mark[markIndex])  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb'] 
    for i in range(k):                                                                                    
        plt.plot(centers[i][0], centers[i][1], mark[i], markersize = 12) 

    mark = ['+b', 'sb', 'db', '<b', 'pb','Dr', 'Db', 'Dg', 'Dk', '^b'] 

    #for i in range(k):                                                                                   
    #    plt.plot(init_centers[i][0], init_centers[i][1], mark[i], markersize = 12) 
    plt.show()


def find_best_k(data_result,K,eplise):
    costs = []
    nrow,ncol = data_result.shape
    for k in xrange(2,K):
        print 'k',k
        centers = [data_result[random.randint(0,nrow-1),0: ncol-1] for i in xrange(k)]
        _,cost,_ = kmeans(data_result,centers,k,eplise)
        costs.append(cost)
    return costs


def plot_cost(cost):
    plt.xlabel('iteration number')
    plt.ylabel('cost value')
    plt.title('curve of cost value')
    klen = len(cost)
    leng = np.linspace(1, klen, klen)
    plt.plot(leng, cost)
    plt.show()    


def initCenters_random(data_result,k):
    nrow,ncol = data_result.shape
    centers = [data_result[random.randint(0,nrow-1),0: ncol-1] for i in xrange(k)]  
    return centers


#def init_centers_max_distance(data_result,k):
#    nrow,ncol = data_result.shape
#    point = np.mean(data_result,axis = 0)[0:ncol-1]
#    centers = [point]
#    for i in xrange(k-1):
#        max_point = find_max_point(data_result,point) 
#        centers.append(max_point)
#        point = np.mean(centers,axis =0)
#    return centers 

def find_min_max_point(data_result,centers):
    nrow,ncol = data_result.shape
    max_distance = 0
    k = len(centers)
    max_distance = 0
    index = -1
    for i in xrange(nrow):
        min_distance = float("inf") 
        for j in xrange(k-1):          
            distance = get_distance(data_result[i,:(ncol-1)],centers[j]) 
            if distance < min_distance:
               min_distance = distance
        if min_distance > max_distance:
            max_distance = min_distance
            point_new = data_result[i,:(ncol-1)]
            index = i
    return point_new,index  

def init_centers_max_distance(data_result,k):
    nrow,ncol = data_result.shape
    random_point = np.mean(data_result,axis = 0)[0:ncol-1]
    centers = [random_point]
    for i in xrange(k-1):
        new_point,index = find_min_max_point(data_result,centers)
        data_result = np.delete(data_result,index,0)
        nnrow,nncol = data_result.shape
        centers.append(new_point)
    return centers

def get_r1(data_array):
    center = np.mean(data_array,axis = 0)
    nrow,ncol = data_array.shape
    d_sum = 0
    for i in xrange(nrow):
        distance = get_distance(data_array[i],center)
        d_sum += distance
    r1 = d_sum / nrow
    return r1


def canopy(data_array,r1):
    r2 = 2 * r1
    k = 0
    centers = []
    clusters = []
    while (len(data_array) != 0 ):
       nrow,ncol = data_array.shape
       init = random.randint(0,nrow-1)
       init_point = data_array[init]
       cluster = []
       indexes = []
       for i in xrange(nrow):
           distance = get_distance(data_array[i],init_point)
           if distance < r2:
              cluster.append(data_array[i])
           if distance < r1:
              indexes.append(i)

       data_array = np.delete(data_array,indexes,0)

       center = np.mean(cluster, axis = 0)
       centers.append(center)
       #print 'cluster',cluster
       clusters.append(cluster)
       k += 1
       #print 'k',k
    return clusters,centers,k 
       

if __name__ == '__main__':
    K = 10
    iter_max = 10
    eplise = 0

    data  = pd.read_csv('/root/Desktop/machineLearning/kmeans/kmeans_test.csv')
    #data = pd.read_csv('http://oheum0xlq.bkt.clouddn.com/kmeans_test.csv')
    data_array = np.array(data)
    nrow,ncol = data_array.shape
    data_result = np.hstack((data_array,np.zeros(nrow).reshape(nrow,1)))
    r1 = get_r1(data_array)
    clusters,centers,k = canopy(data_array,r1)
    print 'clustersL',clusters
    print 'centers',centers
    print 'k',k
    #costs = find_best_k(data_result,K,eplise)
    #plot_cost(costs)

    #k = 4 
    #init_centers = init_centers_max_distance(data_result,k)
    #print 'init_centers',init_centers
    #data_result,costs,centers = kmeans(data_result,init_centers,k,eplise)
    #print 'centers',centers
    #showCluster(data_result,k,centers,init_centers)


