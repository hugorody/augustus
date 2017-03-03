#!/usr/bin/python
#Uses bedtools merged outputs to overlap genes predicted by Augustus
#Component of pipeline_augustus.sh
#usage: python myoverlap.py file1.overlap2 > output.txt

import sys

bedoverlap = sys.argv[1]

try:
    setoverlap = open(bedoverlap)
except IOError:
    print ("Files doesn't exist!")


mydictonezero = dict()                                                  #le o input para criar o primeiro dicionario, onde keys sao genes1 e values sao listas de genes2 
mylist = set()                                                          #cria uma set com todos os genes

for line in setoverlap:
	line = line.split(" ") 
	id_gene1 = line[8].replace("ID=", "")
	id_gene2 = line[17].replace("ID=", "")

	mylist.add(id_gene1)                                                #add gene1 and gene2 to mylist
	mylist.add(id_gene2)
	
	if id_gene1 in mydictonezero:                                       #add to mydictzero
		mydictonezero[id_gene1].append(id_gene2)
	else:
		mydictonezero[id_gene1] = [id_gene2]


mydictone = dict()
num1 = 0

for k in mydictonezero.items():
	mydictone[num1] = k[1]
	mydictone[num1].append(k[0])
	num1 += 1


mydicttwo = dict()                                                      #dicionario que ira receber o overlap final
num2 = 0

for i in mylist:                                                        #para cada gene predito, executa as operacoes abaixo

	retorno = [gene0 for gene0 in mydicttwo.values() if i in gene0]     #verifica se o gene esta no dicionario 2
	if retorno != []:                                                   #se ele estiver no dicionario 2
		for j in retorno:                                               #captura o id do dicionario onde o gene 2 esta
			
			for x in mydicttwo.items():
				x0 = x[0]
				x1 = x[1]
				if j in x1:
					mydicttwo[x0].append(i)                             #insere o gene no dicionario 2
					
					
					
	else:                                                               #se o gene nao estiver no dicionario 2
		
		
		
		retorno2 = [gene1 for gene1 in mydictone.values() if i in gene1]   #verifica se o gene esta no dicionario 1 e ao mesmo tempo cria uma lista para cada uma linha onde o gene esta (lista de listas)
		
		if retorno2 != []:                                              #se encontrar o gene em alguma key do dicionario 1
		
			mysun = []

			for jj in retorno2:
				mysun.extend(jj)
			
			sunset = list(set(mysun))                                   #cria uma lista de genes com todos os outros genes que fazem overlap com o gene 'i'
			
			moonrise = []                                               #lista contendo os valores de sunset que ja estao no dicionario 2
			
			for ji in sunset:                                           #verifica se algum elemento do sunset esta no dicionario 2 e add ao moonrise
				
				retorno3 = [gene2 for gene2 in mydicttwo.values() if ji in gene2]
							
				moonrise.extend(retorno3)
				
			
					
			if moonrise != []:                                          #se moonrise for diferente de vazio, significa um ou mais genes que fazem overlap com "i" ja foram anteriormente inseridos no dicionario 2. Assim, o gene "i" deve ser incorporado a mesma key no dicionario 2
								
				for xz in mydicttwo.items():
					xz0 = xz[0]
					xz1 = xz[1]
					
					if moonrise[0][0] in xz1:                           #usa o primeiro registro de moonrise pra encontrar a respectiva key no dicionario 2 onde o gene "i" sera adicionado
						mydicttwo[xz0].append(i)
						
			else:                                                       #se o moonrise estiver vazio, a lista gerada para o gene "i" sera adicionada ao dicionario 2
				
				mydicttwo[num2] = sunset
				num2 += 1

		
		
for line1 in mydicttwo.values():
	print line1                                                         #imprime resultado
