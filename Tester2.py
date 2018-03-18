from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from nltk.stem import *
import os
from pprint import pprint
import operator
import pickle
from math import log
import string

class Tester():

	def __init__(self,testDocument):
		

		#######
		# Test document
		self.testDocument = testDocument

		# Load Trainer
		self.Trainer = pickle.load(open('./Prob.p','rb'))

		# Temp vars for testing
		self.numcorrect=0
		self.numtotal=0

		# K value for laplace smoothing
		self.k = .05
	
		# Predictions dictionary
		self.predictions = dict(self.Trainer.total_words_in_doc) 
		for cat in self.predictions:
			self.predictions[cat] = 0

		
	def test_document(self,filetest,filecheck):
		# Track encountered words so no double counting
		encountered_words = {}

		# Count of unknown words in document
		other_words = dict(self.predictions)

		# Initialize
		for cat in other_words:
			other_words[cat] = 0

		# Opens file
		f = open(filetest,"r")

		# Splits document into tokens
		tokens = word_tokenize(f.read())

		# Stem the tokens
		stemmer = PorterStemmer()

		for token in tokens:
			# Stem
			token = stemmer.stem(token)

			# Exclude any punctuation
			if token not in encountered_words and token not in list(string.punctuation):
				# Update encountered words
				encountered_words[token] = True
			

			for cat in self.Trainer.diff_words_per_doc_count:
				if token not in self.Trainer.diff_words_per_doc_count[cat] and token not in list(string.punctuation):
					
					# Increase count of unknown words
					other_words[cat] +=1
				else:
					if token not in list(string.punctuation):
						# Computes predictions for known words
						self.predictions[cat] += log((self.Trainer.diff_words_per_doc_count[cat][token]+self.k)/(self.Trainer.total_words_in_doc[cat]+(self.k*len(encountered_words))))

		for cat in self.predictions:
			# Computes predictions for unknown words
			self.predictions[cat]+=(log(self.k/(self.Trainer.total_words_in_doc[cat]+(self.k*len(encountered_words))))*other_words[cat])
		
		# Make the actual guess
		guess = max(self.predictions.iteritems(), key=operator.itemgetter(1))[0] 

		# CHANGE TO FILE
		print(filetest)
		print(guess)
		print(filecheck)
		if(guess==filecheck):
			self.numcorrect+=1
			self.numtotal+=1
		else:
			self.numtotal+=1
			#self.wrong_choice_num[guess]+=1
		print('-'*30)
		for cat in self.predictions:
			self.predictions[cat] = 0

		
		



	def execute_tests(self):
		# Open files with test documents
		f = open(self.testDocument,"r")

		# Puts training documents into list
		docs = f.readlines()

		os.chdir('TC_provided')
		for document in docs:
			# [filepath, category]
			self.test_document(document.split()[0],document.split()[1])

		print(float(self.numcorrect)/float(self.numtotal))
		
		







