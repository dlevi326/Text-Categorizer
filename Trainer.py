from __future__ import division, print_function  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize
from nltk.stem import *
import os
from pprint import pprint
import operator
from math import log
import pickle

class Trainer():
	def __init__(self,filelist):
		# Gets the file list
		self.filelist = filelist 

		# Keeps track of number of docs in each category
		#self.total_docs = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0} 
		self.total_docs = {} 

		# Keeps track of words per category per document
		#self.words_per_doc = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
		self.words_per_doc = {}

		# K value for laplace smoothing
		self.k = 1

		# Keeps track of current encountered words in documents
		# Is reset for every document
		self.encountered_words = {}

		# Final probabilities
		#self.final_probabilities = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		self.final_probabilities = {}

		# Computed probabilities of categories
		self.predictions = {}



	def populate_table(self,trainfile,category):
		# Opens individual file
		f = open(trainfile,'r')

		# Tokenizes documents
		tokens = word_tokenize(f.read())

		# Stemmer
		stemmer = PorterStemmer()

		# Add category to dictionary
		if category not in self.words_per_doc:
			self.words_per_doc[category] = {}
			self.total_docs[category] = 0
			self.final_probabilities[category] = 0
			self.predictions[category] = 0

		# Increases number of documents in the category
		self.total_docs[category]+=1

		for token in tokens:

			# Stems token
			token = stemmer.stem(token)

			if token not in self.encountered_words:
				# Add to list of documented words
				self.encountered_words[token] = True

				# Add to words in category
				if token not in self.words_per_doc[category]:
					self.words_per_doc[category][token] = 1
				else:
					self.words_per_doc[category][token]+=1
		self.encountered_words = {}

	def handle_files(self):

		# Opens training files
		f = open(self.filelist,"r")

		# Puts all training docs into var docs
		docs = f.readlines()

		# [filepath, category]
		os.chdir('TC_provided')
		for document in docs[0:400]:
			self.populate_table(document.split()[0],document.split()[1])

		#pprint(self.words_per_doc['Cri'])
		#for key, value in sorted(self.words_per_doc['Cri'].iteritems(), key=lambda (k,v): (v,k)):
		#	print ("%s:%s" % (key,value))

		# Save object for later use
		pickle.dump(self,open('../Prob.p','wb'))



	'''

	def __init__(self,filelist):
		self.filelist = filelist
		self.total_docs = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}
		self.category_word_per_doc = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
		self.encountered_words={"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
		self.k = 0.056
		self.total_encountered_words = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}

	#words_in_categories = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
	final_probabilities = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}

	def populate_table(self,trainfile,category):
		f = open(trainfile,"r")
		tokens = word_tokenize(f.read())
		stemmer = PorterStemmer()
		self.total_docs[category]+=1
		
		for token in tokens:
			toke = stemmer.stem(token)
			if toke not in self.encountered_words[category]:
				self.encountered_words[category][toke] = True
				if toke in self.category_word_per_doc[category]:
					self.category_word_per_doc[category][toke]+=1
				else:
					self.category_word_per_doc[category][toke]=1

			if toke not in self.total_encountered_words[category]:
				self.total_encountered_words[category][toke] = True
			#else:
				#self.category_word_per_doc[category][toke]+=1
		self.encountered_words = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
			
		


	def handle_files(self):
		f = open(self.filelist,"r")
		docs = f.readlines() # Puts all training docs into var docs
		# [filepath, category]
		os.chdir('TC_provided')
		for document in docs[0:300]:
			self.populate_table(document.split()[0],document.split()[1])

		vocab = self.total_encountered_words

		for cat in self.category_word_per_doc:
			for word in self.category_word_per_doc[cat]:
				self.final_probabilities[cat][word] = log(float(self.category_word_per_doc[cat][word]+self.k)/(float(self.total_docs[cat]+(len(vocab[cat])*self.k))))

		pprint(self.final_probabilities)

		for cat in self.final_probabilities:
			self.final_probabilities[cat]['**other_word**']= log(float(self.k)/(float(self.total_docs[cat]+(len(vocab[cat])*self.k))))
		pickle.dump(self.final_probabilities,open('../Prob.p','wb'))
		for key, value in sorted(self.final_probabilities['Str'].iteritems(), key=lambda (k,v): (v,k)):
			print ("%s:%s" % (key,value))
		print(self.final_probabilities['Cri']['**other_word**'])
		print(self.final_probabilities['Cri']['israel'])
		'''







