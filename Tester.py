from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from nltk.stem import *
import os
from pprint import pprint
import operator
import pickle
from math import log

class Tester():

	def __init__(self,testDocument):
		self.testDocument = testDocument
		self.tester = pickle.load(open('./Prob.p','rb'))
		self.numcorrect=0
		self.numtotal=0
		self.wrong_choice_num = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		self.other_words = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		self.vocab_of_doc = 0
		self.k = 1
		
	def test_document(self,filetest,filecheck):
		encountered_words = {}		
		predictions = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		f = open(filetest,"r")
		tokens = word_tokenize(f.read())
		stemmer = PorterStemmer()
		current_word_count = {}
		for token in tokens:
			token = stemmer.stem(token)
			current_word_count[token] = True
			for cat in predictions:
				if token not in self.tester.words_per_doc[cat]:
					self.other_words[cat] += 1#self.final_probabilities[cat]['**other_word**']
					continue
				else:
					predictions[cat] += log((self.tester.words_per_doc[cat][token]+self.k)/(self.tester.total_docs[cat]+(self.k*len(current_word_count))))
				
				predictions[cat]+=(log(self.k/(self.tester.total_docs[cat]+(self.k*len(current_word_count))))*self.other_words[cat])

		print('-'*30)
		#print(filetest)
		pprint(predictions)
		guess = max(predictions.iteritems(), key=operator.itemgetter(1))[0] 
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
		



	def execute_tests(self):
		f = open(self.testDocument,"r")
		docs = f.readlines() # Puts all training docs into var docs
		# [filepath, category]
		os.chdir('TC_provided')
		for document in docs[701:800]:
			self.test_document(document.split()[0],document.split()[1])
			self.other_words = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		print(float(self.numcorrect)/float(self.numtotal))
		print('Wrong choices: ')
		print(self.wrong_choice_num)







