#!/usr/bin/python

import sys
import operator

filegff1 = sys.argv[1]   #gffmaster.gff
fileover = sys.argv[2]

set_gff1 = set(line.strip() for line in open (filegff1, 'r'))
set_over = set(line.strip() for line in open (fileover, 'r'))

output1 = open("overlap6.fas","w")

sizecatalog = {}
gffcatalog = {}
#fascatalog = {}

for i in set_gff1:
	if "gene" in i and "ID=" in i:
		i = i.split("\t")
		idg = i[8].replace("ID=", "")
		everything = i[1:]
#		seq = i[10]
		startg = int(i[3])
		stopg = int(i[4])
		sizeg = stopg - startg
		
		sizecatalog[idg] = sizeg
		gffcatalog[idg] = everything
#		fascatalog[idg] = seq
	
#		print i,startg,stopg,sizeg

for j in set_over:
	j = j.rstrip()
	j = j.split(" ")
	
	myids = {}
	
	for u in j:
		myids[u] = sizecatalog[u]
	
	larger = max(myids.iteritems(), key=operator.itemgetter(1))[0]
	
	print larger," ".join(gffcatalog[larger])+";"+"Matches="+",".join(j)
#	output1.write(">"+larger+"\n"+fascatalog[larger]+"\n");
