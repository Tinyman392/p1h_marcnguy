'''
python merge.py [file 1] [file 2]
'''

from sys import argv

def loadFile(fName):
	f = open(fName)

	fContents = {}
	for i in f:
		i = i.strip('\n').split(',')
		s = str(i[0:3])
		fContents[s] = i

	f.close()

	return fContents

def printArr(arr):
	line = ""
	for i in arr:
		line += i + ','

	print line[0:-1]

f1 = loadFile(argv[1])
f2 = loadFile(argv[2])

keys = []

for i in f1:
	if i not in keys and i in f2:
		keys.append(i)

for i in f2:
	if i not in keys and i in f1:
		keys.append(i)

print "header"
for i in keys:
	arr = f1[i] + f2[i][3:]
	printArr(arr)

