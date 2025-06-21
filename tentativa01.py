import pandas
import itertools
import time

### Definição da Tabela Hash, Estrutura 1
class HashTable: 
    def __init__(self, size):
        # Construtor
        # ht = HashTable(N), onde N é o tamanho da tabela a ser construída
        self.size = size
        self.table = [[] for i in range(size)]
    
    def _hashFunc(self, key):
        # Função de Hash, retorna índice da tabela
        return key % self.size

    def insert(self, entry):
        # Insere entrada na tabela 
        # Cada entrada é uma lista, onde o primeiro valor é a chave 
        # E outros valores são dados satélite
        index = self._hashFunc(entry[0]) 
        self.table[index].append(entry)
    
    def search(self, key):
        # Procura pela entrada de chave key
        # Retorna toda a entrada 
        # Caso não encontrada, retorna False
        index = self._hashFunc(key) 
        for entry in self.table[index]:
            if key == entry[0]:
                return entry
        # chave não encontrada
        return False


### Definição da Tabela Hash, Estrutura 3, 4 e P3
class ListHashTable: 
    """ É uma tabela hash na qual múltiplos elementos podem
    ser inseridos com uma mesma chave
    estes são colocados em uma lista
    keytype é uma string, 'int' por padrão ou 'str'"""
    def __init__(self, size, keytype='int'):
        # Construtor
        self.size = size
        self.table = [[] for i in range(size)]
        self.keytype = keytype
    
    def _intHash(self, key):
        # Função de Hash para int
        return key % self.size
    
    def _strHash(self, key):
        # Função de Hash para string
        hash = 0
        for char in key:
            hash = (hash*37 + ord(char)) % self.size
        return hash
    
    def insert(self, key, value):
        """Insere entrada na tabela 
        Se key não for achada, insere na tabela como (chave, {conjunto de valores})
        Se key achada, insere value nesse conjunto de valores"""
        if self.keytype == "str":
            index = self._strHash(key)     
        else:
            index = self._intHash(key) 
        for item in self.table[index]:
            if key == item[0]:
                item[1].add(value)
                return
            
        self.table[index].append((key, {value}))
    
    def search(self, key):
        """Procura pela entrada de chave key
        Retorna a lista de valores encontrada
        Caso não encontrada, retorna False"""
        if self.keytype == "str":
            index = self._strHash(key)     
        else:
            index = self._intHash(key) 

        for entry in self.table[index]:
            if key == entry[0]:
                return entry[1]
        # chave não encontrada
        return False



# ===========================
#  CONSTRUÇÃO DAS ESTRUTURAS
# ===========================

print("Começo")
start_time = time.perf_counter()

### Leitura de movies.csv
movies_file = pandas.read_csv("./movies.csv", 
                              dtype={"movieId":int, "title":str, "genres": str, "year": int})
# Construção da tabela hash
movies_hash = HashTable(3000)
for row in movies_file.itertuples(index=False):
    movie_list = list(i for i in row)
    movie_list.extend([0, 0])
    movies_hash.insert(movie_list)


### Leitura de ratings.csv
ratings_file = pandas.read_csv("./ratings.csv", 
                               usecols=["userId", "movieId", "rating"], 
                               dtype={"userId":int, "movieId":int, "rating":float})
# Construção da estrutura 3
ratings_hash = ListHashTable(150000)
for row in ratings_file.itertuples(index=False):
    ratings_hash.insert(row[0], (row[1], row[2]))


# Leitura de tags.csv
tags_file = pandas.read_csv("./tags.csv", 
                            usecols=["movieId","tag"], 
                            dtype={"movieId":int, "tag":str})
# Construção da estrutura 4
tags_hash = ListHashTable(40000, keytype='str')
for row in tags_file.itertuples(index=False):
    tags_hash.insert(row[1], row[0])


end_time = time.perf_counter()
build_time = (end_time - start_time)*1000
print(build_time)
# ========================
#         TESTES
# ========================
if __name__ == "__main__":
    #print(movies_hash.search(1))
    #print(movies_hash.search(221))
    #print(movies_hash.search(131262))
    """
    print(pandas.DataFrame(ratings_hash.search(1), columns=["MovieId", "Rating"]))
    #print(ratings_hash.search(99))
    #print(ratings_hash.search(91))

    for i in range(1, 92):
        if len(ratings_hash.search(i)) != len(set(ratings_hash.search(i))):
            print("Diferente!")
            print(ratings_hash.search(i))

    print("Fim")"""

    #print(len(tags_hash.search("tentou sair do clichÃª")) == len(set(tags_hash.search("tentou sair do clichÃª"))))
    #print(tags_hash.search("tentou sair do clichÃª"))
    #print(tags_hash.search("Mark Waters"))
    print(tags_hash.search("dark hero"))

    