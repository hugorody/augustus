#!/usr/bin/python
#usage: python overlap_augustus.py file1.gff3 file2.gff3

import sys

filegff1 = sys.argv[1]
filegff2 = sys.argv[2]

try:
    set_gff1 = open(filegff1)
    set_gff2 = open(filegff2)
except IOError:
    print ("Files doesn't exist!")

name1 = filegff1.replace(".gff3", "")
name2 = filegff2.replace(".gff3", "")

annline1 = dict()

for line in set_gff1:

	if "#" not in line:
		if "gene" in line:
			line = line.split("\t") 
			
			scaffold = line[0]
			b = line[1]
			c = line[2]
			startg = line[3]
			endg = line[4]
			sizeg = int(line[4])-int(line[3])
			f = line[5]
			g = line[6]
			h = line[7]
			j = line[8].rstrip().replace("ID=", "")
				
			annline1[j+"_1"] = scaffold,b,c,startg,endg,sizeg,f,g,h,j
			
			#print j,startg,endg,sizeg
set_gff1.close()

annline2 = dict()

for line in set_gff2:

	if "#" not in line:
		if "gene" in line:
			line = line.split("\t") 
			
			scaffold = line[0]
			b = line[1]
			c = line[2]
			startg = line[3]
			endg = line[4]
			sizeg = int(line[4])-int(line[3])
			f = line[5]
			g = line[6]
			h = line[7]
			j = line[8].rstrip().replace("ID=", "")
				
			annline2[j+"_2"] = scaffold,b,c,startg,endg,sizeg,f,g,h,j

set_gff2.close()

list_of_overlaps = dict()
geneoverlapping = []

for i in annline1.items():
	id1 = i[0]
	value1 = i[1]
	
	scaffold1 = value1[0]
	startg1 = int(value1[3])
	endg1 = int(value1[4])
	sizeg1 = int(value1[5])
	
	overlap = []
	
	if id1 not in geneoverlapping:
		for j in annline2.items():
			id2 = j[0]
			value2 = j[1]
			
			scaffold2 = value2[0]
			startg2 = int(value2[3])
			endg2 = int(value2[4])
			sizeg2 = int(value2[5])
	
			if id1 != id2 and scaffold1 == scaffold2 and ((startg2 >= startg1 and startg2 <= endg1) or (endg2 >= startg1 and endg2 <= endg1)):
	
				overlap += id2.splitlines()
				geneoverlapping += id1.splitlines()
	
		largerdict = {}
		largerdict[id1] = sizeg1
		
		list_sizeg2 = []
		
		for x in overlap:
			largerdict[x] = int(annline2[x][5])
			list_sizeg2.append(int(annline2[x][5]))
		
		if overlap != []:	
			
			greater2 = any(i > int(sizeg1) for i in list_sizeg2)     #is there any overlap gene in gff_2 with size greater than correspondent gne in gff_1? I
#			print greater2
			
			if greater2 == True:
				
				larger = max(largerdict, key=largerdict.get)
				
				del largerdict[larger]
				
				list_of_overlaps[larger] = list(''.join(key) for key in largerdict)
#				print larger,list(''.join(key) for key in largerdict)
				
			else:
				
				del largerdict[id1]
				
				list_of_overlaps[id1] = list(''.join(key) for key in largerdict)
#				print id1,list(''.join(key) for key in largerdict)
		
		else:
			list_of_overlaps[id1] = ['no_overlapping']
#			print id1,"no overlap"
			
print "Number of overlapping genes:",len(set(geneoverlapping))

output1 = open(name1+"_"+name2+".overlap","w")
output1.write("#Longer_length"+"\t"+"Overlapping_genes");

for i in list_of_overlaps.items():
	output1.write(str(i[0])+"\t"+",".join(i[1])+"\n");
	
output1.close()
