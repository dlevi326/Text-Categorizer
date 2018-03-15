from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer import Trainer
from Tester import Tester

if __name__ == "__main__":
	test = Tester('./TC_provided/corpus1_train.labels')
	test.execute_tests()