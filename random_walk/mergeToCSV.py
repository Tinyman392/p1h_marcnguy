'''
python mergeToCSV.py [csv] [random walks]
'''

from sys import argv

f = open(argv[2])

molHsh = {}
for i in f:
	i = i.strip('\n').split('[')
	i[1] = i[1].strip(']')
	i[1] = i[1].split(',')
	# for j in range(0,len(i[1])):
	# 	i[1][j] = i[1][j].strip()

	i[0] = i[0].strip()

	molHsh[i[0]] = i[1]

f.close()

f = open(argv[1])

print "NSC,GROWTH,LCONC,RAND_WALK"
for i in f:
	i = i.strip('\n').split(',')
	i = i[0:3]
	try:
		i = i + molHsh[i[0]]
		for j in range(0,len(i)):
			i[j] = float(i[j])
	except:
		continue

	print str(i)[1:-1]

f.close()