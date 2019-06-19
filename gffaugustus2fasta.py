#!/usr/bin/python3
#parse GFF output from Augustus and extract FASTA sequences of proteins

import sys

in_file = sys.argv[1]

genes = {} #final catalog of predicted genes
parse = 0
beg = 0
with open(in_file,"r") as set1:
    for i in set1:
        i = i.rstrip()

        if "gene" in i and "#" not in i:
            i = i.split("\t")
            if i[2] == "gene":
                mygene = i[-1]
                s = []

        if "protein sequence" in i: #select protein sequences
            parse = 1
            beg = 1
            i = i.split(" ")
            if "]" in i[-1]:
                s.append(i[-1].replace("]","").replace("[",""))
                genes[mygene] = "".join(s)
                parse = 0
            else:
                s.append(i[-1].replace("[",""))
        else:
            beg = 0

        if parse == 1 and beg != 1:
            i = i.split()
            if "]" in i[-1]:
                s.append(i[-1].replace("]",""))
                parse = 0
                genes[mygene] = "".join(s)
            else:
                s.append(i[-1])

output = open(in_file + ".fas","w")
for i in genes.items():
    output.write(">"+i[0]+"\n"+i[1]+"\n")
