#STRINGS
#lower = palavras em minusculo
#upper = palavras em maiusculo
#count = conta letras
#find = encontra letras ou palavras
#replace = substitui palavras
#voce pode somar palavras
#f string = voce pode juntar palavras formato: f'{}'
#dir = mostra as funcoes que pode ser usadas em uma variavel ou objeto
#help = mostra como usar a funcao 
#type = mostra o tipo da variavel
#len = conta o tamanho da variavel


#operadores matematicos
# + = soma 
# - = subtracao
# * = multiplicacao
# / = divisao
# // = divisao inteira
# ** = potencia
# % = resto da divisao
# == = igual
# != = diferente
# > = maior
# < = menor
# >= = maior ou igual
# <= = menor ou igual
# and = e
# or = ou
# not = nao
# in = esta em
# not in = nao esta em
# is = e
# is not = nao 
#abs = valor absoluto(modulo)
#round = arredondamento
#cast = conversao de tipos

#LISTAS são mutaveis
#usa colchetes [] para criar uma lista 
#apend = adiciona um item a lista ex: lista.append('item')
#insert = adiciona um item a lista em uma posicao especifica ex: lista.insert(0, 'item')
#extend = adiciona varios itens a lista ou outra lista ex: lista.extend(['item1', 'item2'])
#remove = remove um item da lista ex: lista.remove('item')
#pop = remove o ultimo item da lista ex: lista.pop()
#reverse = inverte a lista ex: lista.reverse()
#sort = ordena a lista ex: lista.sort()
#sort(reverse=True) = ordena a lista de forma decrescente
#sorted = ordena a lista sem alterar a lista original ex: sorted(lista)
#min = menor valor da lista
#max = maior valor da lista
#sum = soma dos valores da lista
#index = retorna o indice do valor ex: lista.index('valor')
#in = verifica se o valor esta na lista ex: 'valor' in lista
#enumerate = retorna o indice e o valor da lista ex: for indice, valor in enumerate(lista)
#join = junta os valores da lista ex: ' '.join(lista)
#split = separa os valores da lista ex: 'valor1 valor2 valor3'.split()

#TUPLAS sao imutaveis
#usa parenteses () para criar uma tupla ex: tupla = (1,2,3,4,5)

#SETS sao mutaveis e nao aceitam valores duplicados
#usa chaves {} para criar um set ex: set = {1,2,3,4,5}
#nao se importa com a ordem dos valores ex
#intersection = interseccao de sets ex: set1.intersection(set2)
#difference = diferenca de sets ex: set1.difference(set2)
#union = uniao de sets ex: set1.union(set2)

#dictionary do tipo chave e valor, que significa que cada elemento do dicionario é um par chave/valor.
#usa chaves {} para criar um dicionario ex: dicionario = {'chave1': 'valor1', 'chave2': 'valor2'}
#get = retorna o valor da chave ex: dicionario.get('chave1')
#podemos adicionar um novo valor a chave ex: dicionario['chave3'] = 'valor3'
#pop = remove a chave e o valor ex: dicionario.pop('chave1')
#popitem = remove a ultima chave e valor do dicionario
#update = adiciona um dicionario a outro ex: dicionario.update({'chave4': 'valor4'})
#del = deleta a chave e o valor ex: del dicionario['chave1']
#keys = retorna as chaves do dicionario ex: dicionario.keys()
#values = retorna os valores do dicionario ex: dicionario.values()
#items = retorna os itens do dicionario ex: dicionario.items()
#clear = limpa o dicionario ex: dicionario.clear()

#estruturas de controle
#if = se ex: if condicao: 
#elif = senao se ex: elif condicao:
#else = senao ex: else:
#while = enquanto ex: while condicao:

#operadores de comparacao
# == = igual
# != = diferente
# > = maior
# < = menor
# >= = maior ou igual
# <= = menor ou igual
#is (ve se os objetos estao na mesma posicao de memoria)
#and = e
#or = ou
#id = retorna a posicao de memoria do objeto

#False values
#False
#None
# 0 
# qualquer sequencia vazia ex: '', [], (), {}
#qualquer objeto vazio ex: set(), dict(), etc

#loops
#while = enquanto ex: while condicao: ex
#while True: 
#for = para ex: for item in lista: 
#break = para o loop ex: if condicao: break
#continue = pula a iteracao ex: if condicao: continue
#range = gera uma sequencia de numeros ex: range(10) ex: range(1,10) ex: range(1,10,2)

#funcoes
#def = define uma funcao ex: def nome_da_funcao():
#pass = nao faz nada
#format = formata uma string ex: 'nome: {}'.format('valor')
#return = retorna um valor ex: return valor
#args = argumentos ex: def nome_da_funcao(*args):
#passa uma * para "desempacotar" a lista
#passa duas ** para "desempacotar" o dicionario
#kwargs = argumentos nomeados ex: def nome_da_funcao(**kwargs):

#importar modulos significa que voce esta importando um arquivo que contem funcoes que voce pode usar, é como se fosse uma biblioteca
# se voce cria um modulo voce pode importar ele em outro arquivo se estiver na mesma pasta ou se voce adicionar o caminho do modulo
#import = importa um modulo ex: import math
#quando vai importar um modulo o compilador procura no diretorio atual, se nao encontrar ele procura numa lista chamada sys.path que contem os diretorios onde o python procura os modulos
#primeiro ele procura no diretorio onde o script esta sendo executado
#terceiro ele procura nos diretorios padrao do python
#segundo ele procura nos diretorios que estao na variavel de ambiente PYTHONPATH
#quarto ele procura pacotes de sites de terceiros que voce instalou
#podemos adicionar modulos na sys.path para que o python possa encontra-los sys.path.append('caminho_do_modulo'), mas isso nao é recomendado 
#podemos adicionar modulos na variavel de ambiente PYTHONPATH para que o python possa encontra-los 
#as = renomeia um modulo ex: import math as m
#from = importa um modulo especifico ex: from math import sqrt (importa apenas a funcao sqrt do modulo math)

#Python OOP

#CLASSES
#classes sao como um molde para criar objetos
# variaveis de instancia x variaveis de classe
#variaveis de instancia sao unicas para cada objeto
#variaveis de classe sao compartilhadas entre todos os objetos
#ex: class Pessoa:
#não há beneficios para criar a classe manualmente, para melhorar isso podemos usar o metodo __init__ 
#que é um metodo especial que é chamado quando um objeto é criado
#ex: def __init__(self, nome, idade):
#self é uma referencia ao objeto que esta sendo criado
#nome e idade sao argumentos que passamos para a classe
#ex: pessoa1 = Pessoa('Joao', 20)
#esses argumentos sao chamados de atributos da classe
#podemos adicionar metodos a classe
#ex: def full_name(self):
#return '{} {}'.format(self.nome, self.sobrenome) ou return f'{self.nome} {self.sobrenome}'
#podemos acessar os atributos da classe com self.atributo
#ex: pessoa1.nome
#podemos acessar os metodos da classe com objeto.metodo()
#ex: pessoa1.full_name()
#podemos acessar pela classe tambem ex: Pessoa.full_name(pessoa1)

#__dict__ = mostra os atributos de um objeto ou classe ex: pessoa1.__dict__ que mostra os atributos do objeto pessoa1
#podemos alterar variaveis de classe apenas para um objeto ex: pessoa1.raise_amount = 1.05

#Variaveis de classe
#variaveis de classe sao comuns a todos os objetos
#ex: raise_amount = 1.04
#podemos acessar essas variaveis de classe pela classe ou pelo objeto
#ex: Pessoa.raise_amount ou pessoa1.raise_amount
#podemos acessar essas variaveis de classe dentro da classe com self.raise_amount
#ex: self.pay = int(self.pay * self.raise_amount)
#podemos acessar essas variaveis de classe dentro da classe com a classe
#ex: self.pay = int(self.pay * Employee.raise_amount)
#podemos alterar variaveis de classe apenas para um objeto ex: pessoa1.raise_amount = 1.05
#podemos acessar variaveis de classe com a classe ou com o objeto
#ex: Employee.raise_amount ou pessoa1.raise_amount

#regular methods x class methods x static methods

#para tornar um regular method em um class method 
# a convenção para metodos de classe é (cls)
#  pessoas usam metodos de classe como construtores alternativos, isto é, metodos que criam instancias da classe, maneiras diferentes
# de criar objetos
#ex: @classmethod
#def set_raise_amount(cls, amount):
#cls.raise_amount = amount

#split = separa os valores da lista ex: 'valor1 valor2 valor3'.split()

#class methods x static methods
#class methods passam a classe como primeiro argumento
#static methods nao passam nada como primeiro argumento
#static methods sao metodos que nao usam a classe ou o objeto em nenhum lugar do metodo
#ex: @staticmethod
#def is_workday(day):
# if day.weekday() == 5 or day.weekday() == 6:
# return False
# return True

#heranca e subclasses

#heranca é uma maneira de formar novas classes usando classes que ja foram definidas
#classes que herdam de outra classe sao chamadas de subclasses
#classes que sao herdadas sao chamadas de superclasses
#ex: class Developer(Employee):
#as vezes vamos querer iniciar as subclasses com mais informacoes que a classe pai
#super é uma funcao que chama o metodo da classe pai
#ex: super().__init__(first, last, pay)
#ex: Employee.__init__(self, first, last, pay)
#isintance(objeto, classe) = verifica se o objeto é uma instancia da classe
#issubclass(classe1, classe2) = verifica se a classe1 é uma subclasse da classe2

#metodos especiais ou magic methods
#metodos especiais sao metodos que tem dois underlines antes e depois do metodo
#ex: __init__ __str__ __repr__ __add__ __len__ __getitem__ __setitem__ __delitem__ __iter__ __next__ __contains__ __call__ __enter__ __exit__
#__init__ = inicializa o objeto
#__str__ = retorna uma representacao do objeto é usado para printar o objeto 
#__repr__ = retorna uma representacao do objeto é usado para debugar o codigo
#__add__ = soma dois objetos
#__len__ = retorna o tamanho do objeto
#__getitem__ = retorna um item do objeto
#__setitem__ = altera um item do objeto
#__delitem__ = deleta um item do objeto
#__iter__ = retorna um iterador
#__next__ = retorna o proximo item do iterador
#__contains__ = verifica se um item esta no objeto
#__call__ = chama o objeto como uma funcao
#__enter__ = entra no contexto
#__exit__ = sai do contexto

#property decorators (getters, setters, deleters)
#property decorators permitem que voce acesse um metodo como um atributo 
#ex: @property
#def email(self):
#return '{}.{}@gmail.com'.format(self.first, self.last)

#getters = permite que voce acesse um metodo como um atributo
#ex: @property
#def email(self):
#return '{}.{}@gmail.com'.format(self.first, self.last)

#setter = permite que voce altere um metodo como um atributo
#ex: @property
#def email(self, email):
#first, last = email.split('@')[0].split('.')
#self.first = first
#self.last = last

#deleter = permite que voce delete um metodo como um atributo
#ex: @property
#def email(self):
#del self.email

#file objects
#f = open('arquivo.txt', 'r')
#'r' = leitura
#'w' = escrita
#'a' = escrita no final do arquivo
#'r+' = leitura e escrita
#'w+' = escrita e leitura
#f.close() = fecha o arquivo

#using a context manager
# voce so pode usar ele dentro do bloco with
#with open('arquivo.txt', 'r') as f:
    #f_contents = f.read() = retorna o conteudo do arquivo
    #f_contents = f.readlines() = retorna uma lista com as linhas do arquivo
    #f_contents = f.readline() = retorna a primeira linha do arquivo // se fazer de novo retorna a segunda linha e assim por diante

    #for line in f:
        #print(line, end='') = retorna o conteudo do arquivo
    #isso é mais eficiente pois o python nao precisa carregar o arquivo inteiro na memoria

#se quisermos mais controle sobre o que estamos lendo do arquivo podemos usar o metodo read
#ex: f_contents = f.read(100) = retorna os primeiros 100 caracteres do arquivo
#ex: f_contents = f.read(100) = retorna os proximos 100 caracteres do arquivo e assim por diante

#ex: size_to_read = 100 // teremos que criar uma variavel para controlar o tamanho que queremos ler, mais eficiente
#f_contents = f.read(size_to_read)

# while len(f_contents) > 0:
    #print(f_contents, end='')
    #f_contents = f.read(size_to_read)

#f.tell() = retorna a posicao do cursor no arquivo
#f.seek(0) = move o cursor para o inicio do arquivo ou para a posicao que voce passar

#escrever em arquivos
#f = open('arquivo.txt', 'w') // with open('arquivo.txt', 'w') as f: / ele cria o arquivo se nao existir
#f.write('teste') = escreve no arquivo
#f.write('teste2') = escreve no arquivo logo apos o teste
#f.seek(0) = move o cursor para o inicio do arquivo

#multiplos arquivos

#with open('arquivo.txt', 'r') as rf:
    #with open('arquivo2.txt', 'w') as wf:
        #for line in rf:
            #wf.write(line)

#copiar imagens e arquivos binarios
#with open('imagem.jpg', 'rb') as rf:
    #with open('imagem2.jpg', 'wb') as wf:
        #for line in rf:
            #wf.write(line)

#with = contexto

#conteudos extras

#Slicing listas
#lista[start:stop:step]
#start = onde comeca// stop = onde para// step = quantos passos
#ex: lista[1:5:2] = retorna os valores da lista de 1 a 5 pulando de 2 em 2  
#possui indices positivos e negativos
#ex: lista[-1] = retorna o ultimo valor da lista

#List comprehension
#uma maneira de criar listas de forma mais eficiente
#ex: lista = [i for i in range(10)] = cria uma lista com os valores de 0 a 9
#map = aplica uma funcao a todos os itens de uma lista
#lambda = funcao anonima
#ex: lista = list(map(lambda x: x**2, range(10))) = cria uma lista com os valores de 0 a 9 ao quadrado

#zip = combina duas listas

#dictionary comprehension
#my_dict = {key: value for key, value in zip(keys, values)}

#set comprehension
#my_set = {x for x in 'hello'}

#Sorting lists, tuples and objects
#sorted = ordena a lista sem alterar a lista original ex: sorted(lista)
#sort = ordena a lista ex: lista.sort()
#sort(reverse=True) = ordena a lista de forma decrescente
#key = ordena a lista pelo valor que voce passar ex: lista.sort(key=len)

#lambda = funcao anonima

'''
JSON = JavaScript Object Notation EM PYTHON

json.dumps() = converte um objeto em uma string json
json.dump() = converte um objeto em um arquivo json
json.loads() = converte uma string json em um objeto
json.load() = converte um arquivo json em um objeto

tipos de dados
{key: value} = dicionario
[value] = lista
"string" = string



indent = formata a string json ex: json.dumps(pessoas, indent=2)
'''

#unittest = modulo de teste unitario
#criar um arquivo de teste com o nome test_nome_do_arquivo.py

#OS MODULE
#os.getcwd() = retorna o diretorio atual
#os.chdir() = muda o diretorio ex: os.chdir('caminho')
#os.listdir() = retorna os arquivos do diretorio
#os.mkdir() = cria um diretorio ex: os.mkdir('nome_do_diretorio')
#os.makedirs() = cria varios diretorios ex: os.makedirs('nome_do_diretorio/subdiretorio')
#os.rmdir() = deleta um diretorio ex: os.rmdir('nome_do_diretorio')
#os.removedirs() = deleta varios diretorios ex: os.removedirs('nome_do_diretorio/subdiretorio')
#os.rename() = renomeia um arquivo ou diretorio ex: os.rename('nome_do_arquivo', 'novo_nome_do_arquivo')
#os.stat() = retorna informacoes sobre um arquivo ex: os.stat('nome_do_arquivo')
#os.walk() = retorna um gerador que gera uma tupla com o diretorio, subdiretorios e arquivos ex: os.walk('diretorio')
#for dirpath, dirnames, filenames in os.walk('diretorio'):
    #print('Current Path:', dirpath)
    #print('Directories:', dirnames)
    #print('Files:', filenames)
    #print()

#os.environ.get() = retorna uma variavel de ambiente ex: os.environ.get('HOME')
#os.path.join() = junta diretorios ex: os.path.join(os.environ.get('HOME'), 'teste')
#os.path.basename() = retorna o nome do arquivo ex: os.path.basename('diretorio/arquivo')
#os.path.dirname() = retorna o diretorio ex: os.path.dirname('diretorio/arquivo')
#os.path.split() = retorna o diretorio e o nome do arquivo ex: os.path.split('diretorio/arquivo')
#os.path.exists() = verifica se o arquivo existe ex: os.path.exists('diretorio/arquivo')
#os.path.isfile() = verifica se o arquivo existe ex: os.path.isfile('diretorio/arquivo')






class Employee:

    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@gmail.com'

    def full_name(self):
        return '{} {}'.format(self.first, self.last)
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)


emp_1 = Employee('Joao', 'Silva', 50000)
emp_2 = Employee('Maria', 'Silva', 60000)

print(emp_1.email)
print(emp_2.email)

print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)
 





