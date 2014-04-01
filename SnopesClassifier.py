#!/usr/bin/env python
#coding=utf-8

import nltk
from nltk.classify import NaiveBayesClassifier

class SnopesClassifier:
    
    def __init__(self):

        #map : key - instance id, value - feature_dict
        self.train_map = {}    
        self.labels_list = []
        self.train_list = []

    def run_main(self):
        self.load_input()
        self.pre_process()
        self.train()
        #self.test()
        self.cross_validation()

    def load_input(self):
        #load train features
        with open('training.txt') as train_fd:
            for line in train_fd.readlines():
                line = line and line.strip()
                if not line:continue
                instance_id, feature_id, feature_val = line.split(' ')
                feature_map = self.train_map.setdefault(instance_id, {}) 
                feature_map[feature_id] = feature_val

        #load class labels
        with open('label_training.txt') as labels_fd:
            for line in labels_fd.readlines():
                line = line and line.strip()
                if not line:continue
                self.labels_list.append(line)


    def pre_process(self):
        for key, value in self.train_map.iteritems():
            class_label = self.labels_list[int(key)-1]
            self.train_list.append((value, class_label))
       
        self.train_map = {}
        self.labels_list = []        

    def train(self):
        #self.nb_classifier = NaiveBayesClassifier.train(self.train_list)         
        pass        

    def test(self):
        pass

    def cross_validation(self):

        fold_count = 10
        fold_size = int(len(self.train_list)/fold_count)
                  
        for fcount in range(fold_count):
            start_index = fcount * fold_size
            end_index = start_index + fold_size
            train_features = self.train_list[:start_index] + self.train_list[end_index:]
            test_features = self.train_list[start_index:end_index]    
            
            self.nb_classifier = NaiveBayesClassifier.train(self.train_list)
            print nltk.classify.util.accuracy(self.nb_classifier, test_features)    
         

if __name__ == "__main__":
    sobj = SnopesClassifier()
    sobj.run_main()
