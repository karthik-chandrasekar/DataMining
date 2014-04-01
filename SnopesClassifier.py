#!/usr/bin/env python
#coding=utf-8

import nltk
from nltk.classify import NaiveBayesClassifier

class SnopesClassifier:
    
    def __init__(self):

        #train
        #map : key - instance id, value - feature_dict
        self.train_map = {}    
        self.labels_list = []
        self.train_list = []
        self.train_file = 'training.txt'

        #test
        self.test_map = {}
        self.test_list = []   
        self.test_file = 'testing.txt'     
        self.test_output = 'test_output.txt'

    def run_main(self):
        self.load_input()
        self.pre_process()
        #self.cross_validation()
        self.train()
        self.test()

    def load_input(self):
        #load train features
        self.load_feature_input(self.train_file, self.train_map)

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

    def cross_validation(self):
        fold_count = 10
        fold_size = int(len(self.train_list)/fold_count)
                  
        for fcount in range(fold_count):
            start_index = fcount * fold_size
            end_index = start_index + fold_size
            
            train_features = self.train_list[:start_index] + self.train_list[end_index:]
            test_features = self.train_list[start_index:end_index]    
            
            self.nb_classifier = NaiveBayesClassifier.train(train_features)
            print nltk.classify.util.accuracy(self.nb_classifier, test_features)    
         
    def train(self):
        self.nb_classifier = NaiveBayesClassifier.train(self.train_list)         

    def test(self):
        self.load_feature_input(self.test_file, self.test_map)
        self.pre_process_test_input()
        self.classify_test_input()

    def load_feature_input(self, file_name, input_map):
        with open(file_name) as fd:
            for line in fd.readlines():
                line = line and line.strip()
                if not line:continue
                instance_id, feature_id, feature_val = line.split(' ')
                feature_map = input_map.setdefault(instance_id, {}) 
                feature_map[feature_id] = feature_val
                 

    def pre_process_test_input(self):
        for key, value in self.test_map.iteritems():
            self.test_list.append((value))

        self.test_map = {}

    def classify_test_input(self):
        test_output_fd = open(self.test_output, 'w')  
        for test_case in self.test_list:
            test_output_fd.writelines("%s\n" % (self.nb_classifier.classify(test_case)))
        test_output_fd.close()        


if __name__ == "__main__":
    sobj = SnopesClassifier()
    sobj.run_main()
