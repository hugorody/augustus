#!/usr/bin/python

import sys
import operator

filegff1 = sys.argv[1]   #gffmaster.gff
fileover = sys.argv[2]
filefasta = sys.argv[3]

try:
    f = open(filefasta)
except IOError:
    print ("File doesn't exist!")
    

set_gff1 = set(line.strip() for line in open (filegff1, 'r'))
set_over = set(line.strip() for line in open (fileover, 'r'))

sizecatalog = {}
gffcatalog = {}

for i in set_gff1:
	if "gene" in i and "ID=" in i:
		i = i.split("\t")
		idg = i[8].replace("ID=", "")
		everything = i[1:]
		startg = int(i[3])
		stopg = int(i[4])
		sizeg = stopg - startg
		sizecatalog[idg] = sizeg
		gffcatalog[idg] = everything

	
#create dictionary with all fasta sequences
seqs={}
for line in f:
    line = line.rstrip()
    if line[0] == '>':
        words=line.split() 
        name=words[0][1:]
        seqs[name]=''
    else:
        seqs[name] = seqs[name] + line


outputgff = open("overlap6.gff","w")
outputfasta = open("overlap6.fas","w")

for j in set_over:
	j = j.rstrip()
	j = j.split(" ")
	
	myids = {}
	
	for u in j:
		myids[u] = sizecatalog[u]
	
	larger = max(myids.iteritems(), key=operator.itemgetter(1))[0]
	
	print " ".join(gffcatalog[larger])+";"+"Matches="+",".join(j)
		
	outputfasta.write(">"+larger+"\n"+seqs[larger]+"\n");
