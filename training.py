from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer2 import Trainer
from Tester2 import Tester

if __name__ == "__main__":
	print("Please enter name of training file: ")
	trainingFile = './TC_provided/corpus1_train.labels'
	train = Trainer(trainingFile)
	train.handle_files()