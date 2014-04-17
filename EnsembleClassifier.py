#!/usr/bin/env python
#coding=utf-8

from scipy.sparse import lil_matrix
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier

class EnsembleClassifier:

    def __init__(self):
        
        #Files
        #Inputs
        self.train_file = 'training.txt'
        self.test_file = 'testing.txt'     
        self.label_training_file = 'label_training.txt'
        
        #Output
        self.nb_classifier_output = "nb_classifier_output"
        self.svm_classifier_output = "svm_classifier_output"

        #Sparse Matrix
        self.sparse_matrix = lil_matrix((1843, 26365), dtype=float)
        self.training_labels_list = []

    def load_input(self, filename):
        with open(filename) as file_fd:
            for line in file_fd.readlines():
                yield line

    def main(self):
        self.load_training_data()
        self.load_training_labels()
        self.load_test_data()

    def load_training_data(self):
        for line in self.load_input(self.train_file):
            line = line and line.strip()
            if not line:continue
            try:
                row, col, val = line.split(' ')
                row, col, val = int(row), int(col), float(val)
                self.sparse_matrix[row, col] = val
            except Exception,e:
                print line
    def load_training_labels(self):
        for line in self.load_input(self.label_training_file):
            line = line and line.strip()
            if not line:continue
            line = float(line)
            self.training_labels_list.append(line) 

    def load_test_data(self):
       pass 


if __name__ == '__main__':
    ec = EnsembleClassifier()
    ec.main()

