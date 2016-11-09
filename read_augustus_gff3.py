#!/usr/bin/python
#usage: python read_augustus.py output_augustus.gff3
#read gff file generated as output from Augustus and create two output files. 
#output1 include only gene annotation plus one column more with correspondent sequence
#output2 is a fasta file containing all predicted protein sequences


import sys

filegff = sys.argv[1]

try:
    set_gff = open(filegff)
except IOError:
    print ("File1 doesn't exist!")

outputname = filegff.replace(".gff3", "")

fastaseq = {}
annline = dict()

passing = False
genenumber = 0

for line in set_gff:
	
	if "start gene" in line:
		passing = True
		genenumber += 1
	
	if passing:
		#captures fasta sequence
		if "#" in line and "start" not in line and "end" not in line and "###" not in line:
			line = line.replace("#", "")
			line = line.replace("protein sequence = [", "")
			line = line.replace("]", "")
			line = line.split(" ")
			
			if genenumber not in fastaseq:
				fastaseq[genenumber] = line[1].rstrip()
			else:
				fastaseq[genenumber] = fastaseq[genenumber] + line[1].rstrip()

		#captures gene annotation
		if "#" not in line:
			if "gene" in line:
				line = line.split("\t") 
				a = line[0]
				b = line[1]
				c = line[2]
				d = line[3]
				e = line[4]
				f = line[5]
				g = line[6]
				h = line[7]
				j = line[8].rstrip()
				
				annline[genenumber] = a,b,c,d,e,f,g,h,j
		
	if "end gene" in line:
		passing = False


output1 = open(outputname+"_new_annotation.gff", "w")
for i in annline.keys():
	if i in fastaseq.keys():
		output1.write("g"+str(i)+" "+" ".join(annline[i])+" "+fastaseq[i]+"\n");


output2 = open(outputname+".fas", "w")
for i in fastaseq.items():
	output2.write(">g"+str(i[0])+"\n"+str(i[1]+"\n"));
