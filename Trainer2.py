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
		self.filelist = filelist
		self.total_words = {"Str":0,"Pol":0,"Dis":0,"Cri":0,"Oth":0}

	words_in_categories = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}
	final_probabilities = {"Str":{},"Pol":{},"Dis":{},"Cri":{},"Oth":{}}

	def populate_table(self,trainfile,category):
		encountered_words = {}
		f = open(trainfile,"r")
		tokens = word_tokenize(f.read())
		stemmer = PorterStemmer()
		
		self.total_words[category]+=1
		for token in tokens:
			#word = ''.join(x for x in toke if x.isalpha()) #--> Make words only alpha???
			toke = stemmer.stem(token)
			if toke in encountered_words: #--> Should I add this?
				continue
			else:
				
				encountered_words[toke] = True
				if toke in self.words_in_categories[category]:
					self.words_in_categories[category][toke]+=1
					#self.total_words[category]+=1
				else:
					self.words_in_categories[category][toke] = 1
					#self.total_words[category]+=1
		#pprint(self.words_in_categories)


	def handle_files(self):
		f = open(self.filelist,"r")
		docs = f.readlines() # Puts all training docs into var docs
		# [filepath, category]
		os.chdir('TC_provided')
		for document in docs[0:500]:
			self.populate_table(document.split()[0],document.split()[1])
		for cat in self.words_in_categories:
			for word in self.words_in_categories[cat]:
				self.final_probabilities[cat][word] = log(float(self.words_in_categories[cat][word])/float(self.total_words[cat]))
		pprint(self.final_probabilities)
		#print(max(self.final_probabilities["Str"].iteritems(), key=operator.itemgetter(1))[0])
		
		#print(max(self.final_probabilities["Str"]))
		for cat in self.final_probabilities:
			self.final_probabilities[cat]['**other_word**']= log(float(1)/float(self.total_words[cat]))
		pickle.dump(self.final_probabilities,open('../Prob.p','wb'))
		for key, value in sorted(self.final_probabilities['Str'].iteritems(), key=lambda (k,v): (v,k)):
			print ("%s:%s" % (key,value))



