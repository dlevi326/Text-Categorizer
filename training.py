from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from Trainer import Trainer
from Tester import Tester

if __name__ == "__main__":
	#trainingFile = './TC_provided/corpus3_train.labels'
	trainingFile = raw_input('Please enter the training file: ')
	train = Trainer(trainingFile)
	train.handle_files()