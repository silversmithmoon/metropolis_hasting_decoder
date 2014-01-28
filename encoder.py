import sys, random
from common import *

if __name__ == "__main__":
	charset = [c for c in alphabet]
	random.shuffle(charset)
	encbook = dict(zip(alphabet, charset))
	charlst = []; modelst = []
	with open("test.dat") as testf:
		for line in testf:
			for c in line:
				if c.isdigit():
					charlst.append(encbook['0'])
					modelst.append(c)
				elif c.isalpha():
					charlst.append(encbook[c.lower()])
					modelst.append(c.lower())
				else:
					if len(modelst) == 0 or modelst[-1] != ' ':
						charlst.append(encbook[' '])
						modelst.append(' ')
	comparef = open("compare.dat", "w"); encbookf = open("encbook.dat", "w"); encodedf = open("encoded.dat", "w")
	print >>encbookf, '\n'.join(["%s -> %s" % (c,encbook[c]) for c in alphabet])
	print >>encodedf, ''.join(charlst)
	print >>comparef, ''.join(modelst)
	print >>comparef, ''.join(charlst)
	encbookf.close(); encodedf.close(); comparef.close()
