# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 21:49:01 2016

@author: vjyvtkr
"""

import numpy as np
def two_layers(X,y):
    alphas = [0.001]
    
    # compute sigmoid nonlinearity
    def sigmoid(x):
        output = 1/(1+np.exp(-x))
        return output
    
    # convert output of sigmoid function to its derivative
    def sigmoid_output_to_derivative(output):
        return output*(1-output)
    ''' 
    X = np.array([[0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1]])
                    
    y = np.array([[0],
    			[1],
    			[1],
    			[0]])
    '''
    for alpha in alphas:
        print "\nTraining With Alpha:" + str(alpha)
        np.random.seed(1)
    
        # randomly initialize our weights with mean 0
        synapse_0 = 2*np.random.random((1,50)) - 1
        synapse_1 = 2*np.random.random((50,1)) - 1
        j=-1
        while True:
            j+=1
            # Feed forward through layers 0, 1, and 2
            layer_0 = X
            layer_1 = sigmoid(np.dot(layer_0,synapse_0))
            layer_2 = sigmoid(np.dot(layer_1,synapse_1))
    
            # how much did we miss the target value?
            layer_2_error = layer_2 - y
            err = np.mean(np.abs(layer_2_error))
            if not j%100:
                print "Error after "+str(j)+" iterations:" + str(err)
            if err < 0.1:
                break
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            layer_2_delta = layer_2_error*sigmoid_output_to_derivative(layer_2)
    
            # how much did each l1 value contribute to the l2 error (according to the weights)?
            layer_1_error = layer_2_delta.dot(synapse_1.T)
    
            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
    
            synapse_1 -= alpha * (layer_1.T.dot(layer_2_delta))
            synapse_0 -= alpha * (layer_0.T.dot(layer_1_delta))
    print "Total Iterations =",j
    return [synapse_0,synapse_1]
    
