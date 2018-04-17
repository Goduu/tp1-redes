from socket import *
import sys

# --------------------------------------------
# CODIFICACAO E DECODIFICACAO DOS DADOS

def encode16(entrada):
    return(hex(int(entrada,2)))

def decode16(entrada):
    return(bin(int(entrada,16)))

# --------------------------------------------
# LEITURA DO QUADRO 

quadro = {'length':0, 'checksum':0, 'id':0, 'flags':0, 'dados':'0b0'}

def getQuadroInfo(sequenciaBinaria):
	# sequenciaBinaria: string com todos os dados no formato de enquadramento por contagem
	# considera que os dados no formato:
	# 	SYNC | SYNC | length | chksum | ID | flags | dados
	
	sequenciaBinaria = sequenciaBinaria[2:] # remove o '0b' do inicio
	x = sequenciaBinaria[:16]
	x = int(x, 2) # converte de base 2 para 10
	# x = socket.ntohs(x) # converte de network-order para host-order
	quadro['length'] = x
	
	x = sequenciaBinaria[16:32]
	x = int(x, 2) # converte de base 2 para 10
	quadro['checksum'] = x
	# x = socket.ntohs(x)
	
	x = sequenciaBinaria[32:40]
	x = int(x, 2) # converte de base 2 para 10
	quadro['id'] = x
	# x = socket.ntohs(x)
	
	x = sequenciaBinaria[40:48]
	x = int(x, 2) # converte de base 2 para 10
	quadro['flags'] = x
	# x = socket.ntohs(x)
	
	tamDados = quadro['length']
	quadro['dados'] = sequenciaBinaria[48:(48 + 8*tamDados)]
	# x = socket.ntohs(x)

# ----------------------------------------------


s = socket(AF_INET, SOCK_STREAM)
HOST = "150.164.143.10"
PORT = 33121
s.connect((HOST, PORT))

maximum_bytes = 4096

while True:
	message = input("Your message: ")
	s.send(message.encode('utf-8'))
	print("Awaiting reply\n")
	
	reply = s.recv(maximum_bytes).decode()
	print(reply)

s.close()