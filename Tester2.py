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
		self.testDocument = testDocument
		self.Trainer = pickle.load(open('./Prob.p','rb'))
		self.numcorrect=0
		self.numtotal=0
		self.wrong_choice_num = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		self.k = .05
		self.predictions = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}

		
	def test_document(self,filetest,filecheck):
		encountered_words = {}

		# Count of unknown words in document
		other_words = self.wrong_choice_num

		for cat in other_words:
			other_words[cat] = 0

		

		# Opens file
		f = open(filetest,"r")

		# Splits document into tokens
		tokens = word_tokenize(f.read())

		# Stem the tokens
		stemmer = PorterStemmer()

		#current_word_count = {}
		for token in tokens:

			# Stem
			token = stemmer.stem(token)

			if token not in encountered_words and token not in list(string.punctuation):
				encountered_words[token] = True
			

			for cat in self.Trainer.diff_words_per_doc_count:
				

				if token not in self.Trainer.diff_words_per_doc_count[cat] and token not in list(string.punctuation):
					
					# Increase count of unknown words
					other_words[cat] +=1
					#self.Trainer.predictions[cat] += -10

				else:
					if token not in list(string.punctuation):

						# Computes predictions
						self.predictions[cat] += log((self.Trainer.diff_words_per_doc_count[cat][token]+self.k)/(self.Trainer.total_words_in_doc[cat]+(self.k*len(encountered_words))))
						#self.Trainer.predictions[cat]+=log((self.Trainer.words_per_doc[cat][token])/(self.Trainer.total_docs[cat]+100))

		for cat in self.predictions:
			self.predictions[cat]+=(log(self.k/(self.Trainer.total_words_in_doc[cat]+(self.k*len(encountered_words))))*other_words[cat])
		
		print(other_words)
		print('-'*30)
		#print(filetest)
		pprint(self.predictions)
		guess = max(self.predictions.iteritems(), key=operator.itemgetter(1))[0] 
		# Max or Min???
		print(filetest)
		print(guess)
		print(filecheck)
		if(guess==filecheck):
			self.numcorrect+=1
			self.numtotal+=1
		else:
			self.numtotal+=1
			self.wrong_choice_num[guess]+=1
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

			#self.other_words = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		print(float(self.numcorrect)/float(self.numtotal))
		print('Wrong choices: ')
		print(self.wrong_choice_num)







