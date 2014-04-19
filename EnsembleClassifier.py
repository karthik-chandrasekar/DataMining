#!/usr/bin/env python
#coding=utf-8

from scipy.sparse import lil_matrix
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
import numpy
from sklearn.decomposition import TruncatedSVD

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

        #Results
        self.predicted_labels = None

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

    def reduce_dimension(self, input_matrix):
        #Reducing dimension apparently does not seem to reduce training erros. SO not using it
        svd = TruncatedSVD(n_components=10000, algorithm='randomized', n_iter=5, random_state=None, tol=0.0)
        input_matrix = svd.fit_transform(input_matrix)
        return input_matrix

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
        #self.selectAdaBoostClassifier(fit=1)
        #self.selectRandomForestClassifier(fit=1)
        #self.selectExtraTreesClassifier(fit=1)
        self.selectGradientBoostingClassifier(fit=1)

    def selectAdaBoostClassifier(self, fit=0):
        clf = AdaBoostClassifier(n_estimators=100)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "AdaBoostClassifier  -  %s" % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf, 'AdaBoost')

    def selectRandomForestClassifier(self, fit=0):
        clf = RandomForestClassifier(n_estimators=1000,  max_depth=None, min_samples_split=1, random_state=0, n_jobs=-1)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "RandomForestClassifier - %s" % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf, 'RandomForest')

    def selectExtraTreesClassifier(self, fit=0):
        clf = ExtraTreesClassifier(n_estimators=1000, max_depth=None, min_samples_split=1, random_state=0, n_jobs=-1)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "ExtraTreesClassifie - %s" % scores.mean()
        if not fit==1:return
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf, 'ExtraTrees')

    def selectGradientBoostingClassifier(self, fit=0):
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
        scores = cross_val_score(clf, self.sparse_matrix, self.training_labels_list)
        print "GradientBoostingClassifier - %s"  % scores.mean()
        clf.fit(self.sparse_matrix, self.training_labels_list)
        self.classify_test_data(clf, 'GradientBoosting')

    def classify_test_data(self, clf, clfname):
        self.predicted_labels =  clf.predict(self.test_data)
        self.output_results(clfname)

    def output_results(self, clfname):
        with open("%s_labels" % clfname, 'w') as op_file:
            for i in range(952):
                op_file.write("%s\n" % self.predicted_labels[i])

if __name__ == '__main__':
    ec = EnsembleClassifier()
    ec.main()

