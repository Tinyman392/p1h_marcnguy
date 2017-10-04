from rdkit_to_networkx import *
from random import sample
from sys import stderr
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def parseSMILES(smilesStr):
	mol = Chem.MolFromSmiles(smilesStr)
	atomHsh = {}
	bondHsh = {}

	if mol is None:
		return None, None, None

	for atom in mol.GetAtoms():
		idx = atom.GetIdx()
		arr = [ 
			atom.GetAtomicNum(),
			atom.GetFormalCharge(),
			atom.GetChiralTag(),
			atom.GetHybridization(),
			atom.GetNumExplicitHs(),
			atom.GetIsAromatic()
		]

		for i in range(0,len(arr)):
			try:
				arr[i] = str(arr[i]).split('.')[-1]
			except:
				continue

		atomHsh[idx] = arr

	for bond in mol.GetBonds():
		sIdx = bond.GetBeginAtomIdx()
		eIdx = bond.GetEndAtomIdx()
		bond_type = bond.GetBondType()

		if sIdx not in bondHsh:
			bondHsh[sIdx] = {}
		if eIdx not in bondHsh[sIdx]:
			bondHsh[sIdx][eIdx] = 0
		if eIdx not in bondHsh:
			bondHsh[eIdx] = {}
		if sIdx not in bondHsh[eIdx]:
			bondHsh[eIdx][sIdx] = 0

		try:
			bond_type = bond_type.split('.')[-1]
		except:
			continue

		bondHsh[sIdx][eIdx] = bond_type
		bondHsh[eIdx][sIdx] = bond_type

	return mol, atomHsh, bondHsh

def allVisited(visited):
	for i in visited:
		if not i:
			return False

	return True

def randomWalk(mol, l=10, r=20):
	G = mol_to_nx(mol)

	nodes = nx.nodes(G)
	edges = nx.edges(G)
	
	walks = []
	visited = [False]*len(nodes)

	for i in range(0,r):
		cNode = sample(nodes, 1)[0]
		walk = [cNode]
		visited[cNode] = True
		for j in range(0,l):
			neighborsIter = nx.all_neighbors(G, cNode)
			neighbors = []
			for k in neighborsIter:
				neighbors.append(k)

			try:
				cNode = sample(neighbors, 1)[0]
			except:
				cNode = cNode

			visited[cNode] = True
			walk.append(cNode)
		walks.append(walk)
	
	return walks

def parseWalk(walk, mol, atomHsh, bondHsh):
	mrgArr = []
	for i in range(0,len(walk)):
		f = walk[i]
		arr = []
		try:
			s = walk[i+1]
			if len(bondHsh) > 0:
				arr = atomHsh[f] + [bondHsh[s][f]]
			else:
				arr = atomHsh[f] + ['0']
		except:
			arr = atomHsh[f]

		mrgArr += arr
		
	return mrgArr

def parseWalks(walks, mol, atomHsh, bondHsh):
	arr = []
	for i in walks:
		arr += parseWalk(i, mol, atomHsh, bondHsh)

	return arr

# mol, atomHsh, bondHsh = parseSMILES('C')

# walks = randomWalk(mol)
# arrs = parseWalks(walks, mol, atomHsh, bondHsh)

# print arrs

# cov = len(cov) / float(len(atomHsh))
# print cov

f = open('ChemStructures_Consistent.smiles.txt')
l = 10
r = 12

matrix = []
order = []

for i in f:
	i = i.strip('\n').split('\t')

	mol,atomHsh,bondHsh = parseSMILES(i[1])
	if mol is None:
		# stderr.write(i[1] + '\n')
		continue

	walks = randomWalk(mol, l, r)
	arr = parseWalks(walks, mol, atomHsh, bondHsh)
	matrix.append(arr)
	order.append(i[0])

f.close()

matrix = np.asarray(matrix)
mat_int = LabelEncoder().fit_transform(matrix.ravel()).reshape(*matrix.shape)
del matrix
mat_bin = OneHotEncoder().fit_transform(mat_int).toarray()
del mat_int

for i in range(0, len(mat_bin)):
	print order[i], list(mat_bin[i])
