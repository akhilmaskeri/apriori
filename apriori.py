from optparse import OptionParser

optparser = OptionParser()

optparser.add_option('-f', '--inputFile',dest='input',help='filename containing csv',default="data.csv")
optparser.add_option('-s', '--minSupport',dest='minSupport',help='minimum support value',default=15,type='int')
optparser.add_option('-c', '--minConfidence',dest='minConfidence',help='minimum confidence value',default=20,type='int')

(options, args) = optparser.parse_args()

minSupport = options.minSupport;
minConfidence = options.minConfidence;

transactions = []

with open(options.input,"r") as f:
    for line in f:
        transactions.append( line[:-1].split(",") )

print transactions

def filterMinSupport(dic,minSupport):
	return [ [x] for x in dic if dic[x] >= minSupport]

def filterMinSupportMultiple(dic,minSupport):
	return [ list(x) for x in dic if dic[x] >= minSupport]

def join(items,length):

	x = []
	for itemA in items:
		for itemB in items:
			if len(set(itemA).union(itemB))==length:
				x.append(frozenset(set(itemA).union(itemB)))
	return set(x)


minSupport = (minSupport/100.0) * len(transactions)

frequencySet  = []
itemsList     = []

itemFrequency = {}
assocRules    = {}

# frequency set generation
for transaction in transactions:
	for element in transaction:
		if element in itemFrequency:
			itemFrequency[element] += 1
		else:
			itemFrequency.update({element:1})


items = filterMinSupport(itemFrequency,minSupport)
frequencySet.append(itemFrequency)
itemsList.append(items)

depth = 2

# form subsets of itemsets
while len(items)>1:

	items = join(items,depth)

	# .clear() fails
	itemFrequency = {}

	for e in items:
		for t in transactions:
			if frozenset(e).issubset(t):
				if frozenset(e) in itemFrequency:
					itemFrequency[frozenset(e)] +=1
				else:
					itemFrequency.update({frozenset(e):1})

	
	items = filterMinSupportMultiple(itemFrequency,minSupport)

	itemsList.append(items)
	if len(itemFrequency) > 0 : frequencySet.append(itemFrequency)

	depth+=1


# filter using minimum support and minimum confidence
for i in range(1,len(frequencySet)):
	for e in itemsList[i]:
		support = frequencySet[i][frozenset(e)]/float(len(transactions))
		occurence = 0
		for x in e:
			occurence += frequencySet[0][x]
			
		confidence = support/float(occurence)

		print e,str(int(support*100))+"%",str(int(confidence*100))+"%"
