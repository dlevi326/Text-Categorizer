from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer import Trainer
from Tester import Tester

if __name__ == "__main__":
	print('Please enter the testing file: ')
	testingFile = './TC_provided/corpus3_train.labels'
	test = Tester(testingFile)
	test.execute_tests()