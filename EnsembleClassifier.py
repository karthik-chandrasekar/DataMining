#!/usr/bin/env python
#coding=utf-8

from scipy.sparse import lil_matrix
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
import numpy

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

        #Training data
        self.sparse_matrix = lil_matrix((1842, 26364), dtype=float)
        self.training_labels_list = []

        #Test data
        self.test_data = lil_matrix((952, 26364), dtype=float)

    def load_input(self, filename):
        with open(filename) as file_fd:
            for line in file_fd.readlines():
                yield line

    def main(self):
        #Loading training data
        self.sparse_matrix = self.load_input_data(self.sparse_matrix, self.train_file)

        #Loading training labels
        self.load_training_labels()

        #Loading test data
        self.test_data = self.load_input_data(self.test_data, self.test_file)

        #Classify test data
        self.cross_validation_prediction()


    def load_input_data(self, input_data, input_file):
        for line in self.load_input(input_file):
            line = line and line.strip()
            if not line:continue
            try:
                row, col, val = line.split(' ')
                row, col, val = int(row)-1, int(col)-1, float(val)
                input_data[row, col] = val
            except Exception,e:
                print line
          
        #Convert lil_matrix to normal array
        input_data = input_data.toarray()
        return input_data 

    def load_training_labels(self):
        for line in self.load_input(self.label_training_file):
            line = line and line.strip()
            if not line:continue
            line = int(line)
            self.training_labels_list.append(line) 
        self.training_labels_list = numpy.array(self.training_labels_list)
 
    def cross_validation_prediction(self):
        self.selectAdaBoostClassifier()
        #self.selectRandomForestClassifier()
        #self.selectExtraTreesClassifier()
        #self.selectGradientBoostingClassifier()

    def selectAdaBoostClassifier(self):
        clf = AdaBoostClassifier(n_estimators=100)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "AdaBoostClassifier  -  %s" % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf)

    def selectRandomForestClassifier(self):
        clf = RandomForestClassifier(n_estimators=100,  max_depth=None, min_samples_split=1, random_state=0)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "RandomForestClassifier - %s" % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf)

    def selectExtraTreesClassifier(self):
        clf = ExtraTreesClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0, n_jobs=-1)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "ExtraTreesClassifie - %s" % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf)

    def selectGradientBoostingClassifier(self):
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "GradientBoostingClassifier - %s"  % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf)

    def classify_test_data(self, clf):
        print clf.predict(self.test_data)

if __name__ == '__main__':
    ec = EnsembleClassifier()
    ec.main()

