#read NCBI IDs in a BLAST result file, formatted with outfmt 6, and captures PDB information about the reference sequence
# awk '$3>40' = minimum percent identity in blast

cat "$1" | awk '$3>40' | while read line
do

query=`echo "$line" | awk {'print $1'}`
idpdb=`echo "$line" | awk {'print $2'} | sed 's/^gi|.*|.*|\(.*\)|[A-Z]/\1/g'`
body=`echo "$line" | cut -f 3-`

result=`lynx -dump http://www.rcsb.org/pdb/explore/explore.do?structureId="$idpdb"`

gene=`echo "$result" | grep "DOI:" -B 2 | head -1`
classification=`echo "$result" | grep "Classification: \[" | head -1 | sed 's/^.*Classification: \[.*\]//g' | head -1`
gene_names=`echo "$result" | grep "Gene Name(s):" | sed 's/^.*Gene Name(s): //g' | head -1`

echo "$query $idpdb $body [Gene: $gene, Gene Name(s): $gene_names, Classification: $classification]" | sed 's/\t/ /g' | tee -a "$1".annotation.txt

done
