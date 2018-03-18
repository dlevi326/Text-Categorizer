from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer import Trainer
from Tester import Tester

if __name__ == "__main__":
	print("Please enter name of training file: ")
	trainingFile = './TC_provided/corpus3_train.labels'
	train = Trainer(trainingFile)
	train.handle_files()