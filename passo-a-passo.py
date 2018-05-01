# Ordem definida pelo professor:
# Lê arquivo de entrada -> Enquadra -> Codifica -> Transmite -> Recebe -> Decodifica - > Processa quadro -> Grava arquivo de saída
#-------------------------------------------------------------------------------

# Funcao que le texto de um arquivo de entrada lista.txt
def leitura_arquivo():

	# Abre o arquivo de entrada
	filename='../dccnet-test/tests/hello.txt'
	
	with open(filename, 'r+b') as file:
		byte = file.read()
		print(byte)
		#while byte != b'':
		 #   print(byte)
		  #  byte = file.read(1)
		  
	# Codifica
	codificado = encode16(byte)
	
		  
	"""	  
	# Escreve no arquivo de saída
	with open('../dccnet-test/tests/hello2.txt', 'w') as file:
		file.write(codificado)
		print("\n\n---------------chegou ao final--------------")
		
	print("\n\n------------------DECODIFICA--------------")
	decodificado = decode16(codificado)
	print(decodificado)
	print("Comparação com original: ", decodificado==byte)
	"""
	
	# codificado = 'dcc023c2dcc023c2000e00000000' + codificado
	quadro = enquadra(byte)
	print("\n-----QUADRO CODIFICADO------\n",quadro)
	
	header = constroi_checksum(quadro)
	check = checksum(header)
	print("\n------------CHECKSUM: ",check)
	
	# quadro[20:24] = check
	quadrofinal = quadro[:20] + check + quadro[24:]
	
	print("\n------------QUADRO COM CHECKSUM------------\n", quadrofinal)

#-------------------------------------------------------------------------------

# FUNCOES UTEIS:
	# ord('z') retorna valor correspondente ao caractere ascii
	# chr(ord('z')) retorna char correspondente ao valor ascii
	# hex(10) retorna o valor inteiro passado como hexadecimal

	
#-------------------------------------------------------------------------------	
# Funcao que recebe um vetor de bytes e converte para um vetor em base16
def encode16(bytelist):
	hexlist = [hex(x) for x in bytelist]
	newlist = []
	
	for item in hexlist:
		item = item[2:]  # remove o 0x selecionando somente a partir do segundo elemento
		
		if(len(item)==1): # se o valor hexadecimal for tiver apenas 1 caractere
			item = ''.join(['0', item]) # acrescenta 0 antes (ex: 'a'->'0a')
			
		newlist.append(item)
	 
	result = ''.join(newlist) # concatena os valores numa unica string
	return(result)

#-------------------------------------------------------------------------------	
# Funcao que recebe um vetor em base16 e converte para um vetor de bytes
def decode16(base16list):
	
	hexlist = []
	for i in range(0, len(base16list), 2):
		hexlist.append(base16list[i:i+2]) # pega valores de 2 em 2 (ex: dc|c0|23|c2)
	
	hexlist = [''.join(['0x',y]) for y in hexlist] # adiciona o '0x' do hexadecimal
	intlist = [int(x,16) for x in hexlist] # converte para inteiro
	charlist = [chr(x) for x in intlist] # converte para o caractere ascii

	result = ''.join(charlist).encode() # concatena e converte para bytes usando encode()
	return(result)

#-------------------------------------------------------------------------------
# Recebe o quadro codificado como base 16 e com campo checksum 0
def constroi_checksum(codificado16):
	
	header = []
	for i in range(0, len(codificado16), 2):
		header.append(codificado16[i:i+2])
	return(header)

#-------------------------------------------------------------------------------
# Function:    checksum
# Author:      Grant Curell
# Created:     16 Sept 2012
# Description: Calculates the checksum for an IP header
#-------------------------------------------------------------------------------
    
def checksum(header):

    size = len(header)
    cksum = 0
    pointer = 0
    
    #The main loop adds up each set of 2 bytes. They are first converted to strings and then concatenated
    #together, converted to integers, and then added to the sum.
    while size > 1:
        cksum += int(header[pointer] + header[pointer+1], 16)
        size -= 2
        pointer += 2
    if size: #This accounts for a situation where the header is odd
        cksum += header[pointer]
        
    cksum = (cksum >> 16) + (cksum & 0xffff)
    cksum += (cksum >>16)
    result = (~cksum) & 0xffff
    result = hex(result)[2:]
    
    return result

#-------------------------------------------------------------------------------

# Funcao que recebe dados como bytes e retorna o quadro no formato encode16.
#  OBS: campo do checksum vale '0000' e sera calculado externamente.
def enquadra(dados_byte):
	sync = 'dcc023c2'
	length = len(dados_byte) #TODO: usar network byte order
	
	length = encode16([length])
	n = 4 - len(length)
	length = '0'*n + length
	
	checksum = '0000'
	ID = '00'
	flags = '00'
	
	dados16 = encode16(dados_byte)
	
	quadro = ''.join([sync, sync, length, checksum, ID, flags, dados16])
	return(quadro)
	
	

leitura_arquivo()

import sys

print ("This is the name of the script: ", sys.argv[1])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))

print("\nIP:", sys.argv[2][:9], "\nPORT:", sys.argv[2][10:])




