#!/bin/sh
echo "FASTA file for prediction:"; read fastafile
echo "List of Hints files:"; read hintsfiles

########################################################################
#run augustus gene prediction in parallel. One job for each hintfile being used
runaugustus()
{
augustus --species="$line" --gff3=on --cds=on "$fastafile" > augustus_"$idrun".gff3
}

idrun=0
cat "$hintsfiles" | while read line
do
idrun=$(($idrun+1))
runautustus &
done

wait

########################################################################
#rename gene IDs from gff3 files in each of the outputs
for i in *.gff3
do
idaug=`echo "$i" | sed "s/augustus_//g" | sed "s/.gff3//g"`
sed -i "s/ID=\(.\)/ID=$idaug\1/g" "$i"
done


########################################################################
#Run Bedtools for each possible pair amongst GFF3 files
#output: *.overlap2 (the output from bedtools intersect)
#parameters: -f (), -wo ()

for file1 in *.gff3
do

name=`echo "$file1" | sed 's/.gff3//g'`

for file2 in *.gff3
do

num2=`echo "$file2" | sed 's/.gff3//g' | sed 's/augustus_//g'`

bedtools intersect -f 0.50 -wo -a "$file1" -b "$file2" > "$name"_"$num2".overlap

done
done

#Captures only "gene" records from .overlap files and creates a unique file augustus.overlap2 containing all respective records
cat *.overlap | awk '$3="gene"' | awk '$12="gene"' | awk '$9!=$18' | sed '/cds/d' | sed '/Parent/d' > augustus.overlap2

#remove extra .overlap files
rm "$name"*.overlap


#Convert Overlap2 to Overlap3
#input: *.overlap2
#output: *.overlap3
#description: Olverlap3 is a file where each line correspond to overlaps of all 25 files against each of 25 files.


python myoverlap.py augustus.overlap2 > augustus.overlap3


#Convert GFF master and wholeoverlap5 to final file overlap6
#input: GFF master (join all the 25 augustus gff files) and wholeoverlap5.txt
#output: overlap6.gff and overlap6.fas
#description: 

cat *.gff3 > gffmaster.gff

python overlap6.py gffmaster.gff augustus.overlap3 > augustus_finaloverlap.gff
