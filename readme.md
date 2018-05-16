# Apriori Algorithm

Code implementation for Apriori algorithm for fast association analysis.

### Data format
file containing each line as transaction, items separated by comma.

	-f  --inputFile    		data file
	-s  --minSupport		minimum support count in %
	-c  --minConfidence		minimum confidence count in %

### Example use
	python apriory.py -f data.txt -s 60 -c 80

