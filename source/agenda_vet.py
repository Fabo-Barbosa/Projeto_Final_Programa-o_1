# imports
import sys
import pickle
import time
import os

# função que retorna a base de dados inicializada
def getDataBase(dataPath) -> list:
  dados = []

  with open(dataPath, mode='r+', newline='', encoding='utf-8') as arq:
    campos = arq.readline().replace(',', ' ').split()
    conteudo = arq.readlines()

    for i in range(len(conteudo)):
      lista = conteudo[i].strip("\r\n").split(',')
      elemento = {}

      for j in range(len(campos)):
        if campos[j] == "idade":
          elemento[campos[j]] = int(lista[j])
        elif campos[j] == "preço":
          elemento[campos[j]] = float(lista[j])
        else:
          elemento[campos[j]] = lista[j]

        if j == (len(campos) - 1):
          dados.append(elemento)
    arq.close()

  return dados

def mudar_extensao(caminho_arquivo, nova_extensao):
    # Separa o caminho base e a extensão antiga
    base = os.path.splitext(caminho_arquivo)[0]
    
    # Adiciona a nova extensão
    novo_caminho = f"{base}.{nova_extensao.lstrip('.')}"
    
    # Renomeia o arquivo com a nova extensão
    os.rename(caminho_arquivo, novo_caminho)
    
    return novo_caminho

#função para exportar o arquivo para csv ou binário
def exportaArquivo(dataPath) -> str:
  if dataPath == "base_de_dados.csv":
    with open(dataPath, "r+") as arq:
        dados = arq.read()
        arq.close()

    dataPath = mudar_extensao(dataPath, ".bin")

    with open(dataPath, "wb") as arq:
        pickle.dump(dados, arq)
        arq.close()

  else:
    with open(dataPath, "rb") as arq:
        dados = pickle.load(arq)
        arq.close()
    
    dataPath = mudar_extensao(dataPath, ".csv")

    with open(dataPath, "w") as arq:
        arq.write(dados)
        arq.close()
  return dataPath

# função que gera um novo elemento para ser incluido
def gerarElemento() -> dict:
   nome = input("Nome: ").capitalize()
   tipo = input("Tipo: ").capitalize()
   idade = int(input("Idade: "))
   descricao = input("Descricao: ").capitalize()
   data_hora = input("Data e hora [YYYY/MM/DD HH:mm]: ").capitalize()
   preco = float(input("Preço: "))

   campos = ["nome", "tipo_de_animal" ,"idade" ,"descrição" ,"data_e_hora" ,"preço"]
   valores = [nome, tipo, idade, descricao, data_hora, preco]
   elemento = {}

   for i in range(0, len(valores)):
      elemento[campos[i]] = valores[i]

   return elemento

# função printa uma lista de posições que contém a key
def getPosicaoKey(key, dados) -> None:
   count = 0
   print("Posições: ")
   for i in range(0, len(dados)):
      for j in dict(dados[i]).values():
         if str(key).capitalize() == str(j):
            print(i)
            count += 1
   if count == 0:
      print("Chave não encontrada entre os elementos.")

# função para inprimir
# recebe os dados e, ou uma posição, ou um intevalo, ou nada
def imprimir(dados = list[dict], posi = -1, posf = -1):
   if posi == -1:
      for i in range(0, len(dados)):
         print(i, "- ", dados[i])
         print(150*"_")
   else:
      if posf == -1:
         if posi >= 0 or posi < len(dados):
          print(posi, "- ", dados[posi])
         else:
            print("Posição inválida")
      else:
         if (posf >= posi):
          for i in range(posi, posf + 1, 1):
            print(i, "- ", dados[i])
            print(150*"_")
         else:
            print("Intervalo inválido")
  
#estrutura principal
def main() -> int:
  dataPath = "base_de_dados.csv"
  dados = getDataBase(dataPath)
  lista_de_remover = []
  op = -1

  while op != 5:
     tipo = "binário" if dataPath.endswith(".csv") else "csv"
     op = int(input(f"0- Exportar para {tipo}\n1- Inserir\n2- Buscar\n3- Imprimir\n4- Remover\n5- Sair\nOpção: "))

     if op == 0: # opção que exporta o arquivo de entrada para binário ou csv
        print(50*"\n")
        dataPath = exportaArquivo(dataPath)

     elif op == 1: # opção para adicionar um elemento
        print(50*"\n")
        if len(lista_de_remover) > 0: # no caso de existir elementos na lista de remover é removido o primeiro
           dados.pop(lista_de_remover[0])
        dados.append(gerarElemento())
        print(f"Elemento inserido: posição= {len(dados) - 1}\n\n")

     elif op == 2: # opção que mostra todas as posições para uma chave
        print(50*"\n")
        key = input("Digite uma chave para buscar: ")
        getPosicaoKey(key, dados)
        print("\n\n")

     elif op == 3: # opção para imprimir
        print(50*"\n")
        n = int(input("0- Imprimir tudo\n1- Imprimir uma posição\n2- Imprimir um intervalo\nOpção: "))
        if n == 0: # imprimi todos os elementos
           imprimir(dados)
        elif n == 1: # imprimi uma posição específica 
           value = int(input("Posição: "))
           imprimir(dados, value)
        elif n == 2: # imprimi um intervalo de elementos
           value1 = int(input("Inicio: "))
           value2 = int(input("Fim: "))
           imprimir(dados, value1, value2)
        print("\n\n")

     elif op == 4: # adiciona um elemento na lista de remover
        print(50*"\n")
        elemento = int(input("Posição: "))
        lista_de_remover.append(elemento)
   
     elif op == 5: # sai da aplicação caso o usuário submeta 5
        print(50*"\n")
        print("Saindo...")
        time.sleep(3)

     else: # qualquer outro número vai pedir para repetir
        print(50*"\n")
        print("Opeção inválida! Tente outro número...")
  return 0

#execução do código
if __name__ == "__main__":
  sys.exit(main())