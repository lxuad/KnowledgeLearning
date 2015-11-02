import os
import sys
import codecs
import re

#this code will read a each sentence line by line and output an input for ML model
#the format is label \t <index1>:<value1> .... (sparse representation)
#Run by command: python getFeatures.py INPUT_DIRECTORY > OUTPUT

if __name__ == '__main__':
	vocab = {}
	folder_path = sys.argv[1]
	for fname in os.listdir(folder_path):
		f = codecs.open(folder_path+'/'+fname, encoding = 'utf-8')
		for line in f:
			features = {}
			sentence_type = 0
			label = 'false'
			token = line.rstrip().lstrip().split("\t")
			sentence = token[0]

			#get label for each sentence
			if len(token) > 1:
				sentence = token[1]
				if token[0] == '-true':
					label = "true"
				else:
					label = "notsure"

			#set the sentence type: 1 for questions 2 for declarative sentence 3 for exclaimation
			#sentence type is treated as the first feature
			last_char = sentence[len(sentence)-1]
			if last_char == '?':
				sentence_type = 1
			elif last_char == ".":
				sentence_type = 2
			elif last_char == "!":
				sentence_type = 3

			#only consider words that include [0-9a-zA-Z]
			sentence = re.sub("\\W+", " ", sentence, flags = re.UNICODE)
			words = sentence.split()
			if len(words) < 1:
				continue
			for w in words:
				if w not in vocab.keys():
					vocab[w] = len(vocab) + 2
				index = vocab[w]
				if index in features.keys():
					features[index] += 1
				else:
					features[index] = 1
			sys.stdout.write(label+"\t1:"+str(sentence_type)+" ")
			for key in sorted(features):
				sys.stdout.write(str(key)+':'+str(features[key])+" ")
			sys.stdout.write("\n")
