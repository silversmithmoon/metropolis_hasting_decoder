import sys

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
	

def generative_matrix(charlst, modelst):
	vector = {}
	matrix = {}
	charset = set(charlst)
	for m in alphabet:
		matrix[m] = {}
		for c in charset:
			matrix[m][c] = 0.1
	for m,c in zip(modelst, charlst):
		matrix[m][c] += 1
	
	for m in alphabet:
		rsum = sum(matrix[m].values())
		vector[m] = rsum
		for c in charset:
			matrix[m][c] /= rsum
	return vector, matrix
		
def load_matrix(matrixFile):
	matrix = {}
	with open(matrixFile) as f:
		for line in f:
			prev, curr, prob = line.split()
			if prev not in matrix:
				matrix[prev] = {}
			matrix[prev][curr] = float(prob)
	return matrix

