from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer import Trainer
from Tester import Tester

if __name__ == "__main__":
	testingFile = raw_input('Please enter the testing file: ')
	test = Tester(testingFile)
	test.execute_tests()