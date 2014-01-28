# -*- encoding=utf8 -*-
import sys, random, math
from common import *


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', ' ']

def load_decoded(decodedFile):
	charlst = []
	with open(decodedFile) as f:
		for line in f:
			for c in line:
				if c.isalpha():
					charlst.append(c.lower())
				elif c.isdigit():
					charlst.append('0')
				elif len(charlst)==0 or charlst[-1]!=' ':
					charlst.append(' ')
	return charlst

def load_encoded(encodedFile):
	charlst = []
	with open(encodedFile) as f:
		for line in f:
			for c in line[:-1]:
				charlst.append(c)
	return charlst

def tranfer_matrix(charlst):
	matrix = {}
	for cp in alphabet:
		matrix[cp] = {}
		for cc in alphabet:
			matrix[cp][cc] = 0.1

	for i,cc in enumerate(charlst):
		if i == 0: continue
		pc = charlst[i-1]
		matrix[pc][cc] += 1
	
	for cp in alphabet:
		rsum = sum(matrix[cp].values())
		for cc in alphabet:
			matrix[cp][cc] = math.log(matrix[cp][cc]/rsum)
	return matrix
	

def likelihood(charlst, decbook, alpha):
	r = .0
	for i,c in enumerate(charlst):
		pm = ' ' if i == 0 else decbook[charlst[i-1]]
		r += alpha[pm][decbook[c]]
	return r


if __name__ == "__main__":
	trainFile, encodedFile = "train.dat", "encoded.dat"
	alpha = tranfer_matrix(load_decoded(trainFile))
	charlst = load_encoded(encodedFile)
	decbook = dict([(c,m) for c,m in zip(alphabet, alphabet)])
	score = likelihood(charlst, decbook, alpha)
	best_decbook = dict(decbook)
	best_score = score
	
	for n in range(5000):
		r0 = int(random.random() * len(alphabet))
		r1 = int(random.random() * len(alphabet))
		if r0 == r1:
			continue
		decbook[alphabet[r0]], decbook[alphabet[r1]] = decbook[alphabet[r1]], decbook[alphabet[r0]]
		new_score = likelihood(charlst, decbook, alpha)
		if new_score > score:
			score = new_score
			if score > best_score:
				best_decbook = dict(decbook)
				best_score = score
		else:
			if random.random() < math.e ** (new_score - score):
				score = new_score
				print "lower"
			else:
				decbook[alphabet[r0]], decbook[alphabet[r1]] = decbook[alphabet[r1]], decbook[alphabet[r0]]
		print "%03d: score=%8.2f" % (n, score)
	
	decodedf = open("decoded.dat", "w"); decbookf = open("decbook.dat", "w");
	# 输出解码结果
	print >> decodedf, ''.join([decbook[c] for c in charlst])
	
	# 输出码书
	print >> decbookf, '\n'.join(["%s -> %s" % (m,c) for (c,m) in decbook.items()])
