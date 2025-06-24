import pandas
import itertools
import time
import tentativaOrdenacao

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

    def ocupacao(self):
        n_ocupadas = 0
        for list in self.table:
            if len(list) > 0:
                n_ocupadas += 1

        return n_ocupadas / self.size
    
    def tamMaxLista(self):
        max_length = 0
        for list in self.table:
            if max_length < len(list):
                max_length = len(list)
        return max_length

    def tamMedioLista(self):
        sum_lengths = 0
        n_filled = 0
        for list in self.table:
            if len(list) > 0:
                sum_lengths += len(list)
                n_filled += 1
        
        if n_filled == 0:
            return 0
        return sum_lengths / n_filled

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
                item[1].append(value)
                return
            
        self.table[index].append((key, [value]))

    def bulk_insert(self, key, value_list):
        # inserção para vários items de uma mesma chave por vez
        if self.keytype == "str":
            index = self._strHash(key)     
        else:
            index = self._intHash(key) 
        for item in self.table[index]:
            if key == item[0]:
                item[1].extend(value_list)
                return
            
        self.table[index].append((key, value_list))

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
    
    def ocupacao(self):
        n_ocupadas = 0
        for list in self.table:
            if len(list) > 0:
                n_ocupadas += 1

        return n_ocupadas / self.size
    
    def tamMaxLista(self):
        max_length = 0
        for list in self.table:
            if max_length < len(list):
                max_length = len(list)
        return max_length

    def tamMedioLista(self):
        sum_lengths = 0
        n_filled = 0
        for list in self.table:
            if len(list) > 0:
                sum_lengths += len(list)
                n_filled += 1
        
        if n_filled == 0:
            return 0
        return sum_lengths / n_filled    

class TrieNode:
    def __init__(self):
        self.sons = [None for i in range(256)]
        self.movieId = -1

    def insert(self, title, movieId):
        title_fixed = title.encode('latin1', errors='replace').decode('latin1') # para tirar char não ascii
        self._insert(title_fixed, movieId)

    def _insert(self, title, movieId):      
        if len(title) == 0:
            self.movieId = movieId
        else:
            if self.sons[ord(title[0])] == None:
                self.sons[ord(title[0])] = TrieNode()
            self.sons[ord(title[0])]._insert(title[1:], movieId)
    
    def search(self, title):
        title_fixed = title.encode('latin1', errors='replace').decode('latin1') 
        cur_node = self

        for c in title_fixed:
            if cur_node.sons[ord(c)] != None:
                cur_node = cur_node.sons[ord(c)]
            else:
                return -1
        
        return cur_node.movieId
    
    def prefixSearch(self, prefix):
        prefix_fixed = prefix.encode('latin1', errors='replace').decode('latin1') 
        cur_node = self
        # caminha pelo prefixo
        for c in prefix_fixed:
            if cur_node.sons[ord(c)] != None:
                cur_node = cur_node.sons[ord(c)]
            else:
                return list()
        # lista filmes da sub-árvore
        return cur_node.listMovies()


    def listMovies(self):
        # Recursivamente lista filmes a partir de um nodo (inclusive ele)
        movie_list = list()
        if self.movieId != -1:
            movie_list.append(self.movieId)
        
        for son in self.sons:
            if son != None:
                movie_list.extend(son.listMovies())

        return movie_list

            
def pesquisa1(prefixo):
    global movies_hash, title_trie

    idList = title_trie.prefixSearch(prefixo)
    
    if len(idList) == 0:
        print("Sem filmes com este prefixo!")
        return
    
    moviesList = list()
    for id in idList:
        temp_movie = movies_hash.search(id)
        if temp_movie != False:
            moviesList.append(temp_movie)

    if len(moviesList) == 0:
        print("Não há filmes com este prefixo!") 
        return
    
    for movie in tentativaOrdenacao.ordenar_por_nota_global(moviesList):
        print(movie)
    
def pesquisa2(userID):
    global movies_hash, ratings_hash
    
    ratingsList = ratings_hash.search(userID)
    
    if ratingsList == False:
        print("Usuário não fez avaliações.")
        return
    
    moviesList = list()
    for rating in ratingsList:
        temp_movie = movies_hash.search(rating[0])
        if temp_movie != False:
            moviesList.append([*temp_movie, rating[1]])
    
    if len(moviesList) == 0:
        print("Sem filmes avaliados por esse usuário!")
        return
    
    for movie in itertools.islice(tentativaOrdenacao.ordenar_por_nota_usuario_e_global(moviesList), 20):
        print(movie)
    # o que resta fazer é fazer print bonitinho
    
def pesquisa3(n_filmes, genre):
    global movies_hash, genres_hash

    idList = genres_hash.search(genre)
    if idList == False:
        print("Não há filmes deste gênero!")
        return
    
    moviesList = list()
    for id in idList:
        temp_movie = movies_hash.search(id)
        if temp_movie != False and temp_movie[5] >= 1000:
            moviesList.append(temp_movie)
        
    if len(moviesList) == 0:
        print("Não há filmes deste gênero!") 
        return
    
    for movie in itertools.islice(tentativaOrdenacao.ordenar_por_nota_global(moviesList), n_filmes):
        print(movie)
    # o que resta fazer é fazer print bonitinho

def pesquisa4(tag1, tag2):
    global tags_hash, movies_hash
    
    listTag1 = tags_hash.search(tag1)
    listTag2 = tags_hash.search(tag2)

    if listTag1 == False or listTag2 == False:
        print("Tag não existe!")
        return

    intersecSet = set(listTag1).intersection(set(listTag2))

    moviesList = list()
    for id in intersecSet:
        temp_movie = movies_hash.search(id)
        if temp_movie != False:
            moviesList.append(temp_movie)

    if len(moviesList) == 0:
        print("Sem filmes com ambas as tags!")
        return
    
    for movie in tentativaOrdenacao.ordenar_por_nota_global(moviesList):
        print(movie)
    # o que resta fazer é fazer print bonitinho


# ===========================
#  CONSTRUÇÃO DAS ESTRUTURAS
# ===========================

print("Começo")
start_time = time.perf_counter()

### Leitura de movies.csv
movies_file = pandas.read_csv("./movies.csv", 
                            dtype={"movieId":int, "title":str, "genres": str, "year": int})
# Construção da tabela hash
movies_hash = HashTable(10000)
genres_hash = ListHashTable(20, keytype='str')
title_trie = TrieNode()
for row in movies_file.itertuples(index=False):
    movie_list = list(i for i in row)
    movie_list.extend([0, 0])
    movies_hash.insert(movie_list)
    
    for genre in movie_list[2].split("|"):
        genres_hash.insert(genre, movie_list[0])

    title_trie.insert(row[1], row[0])



### Leitura de ratings.csv
ratings_file = pandas.read_csv("./ratings.csv", 
                            usecols=["userId", "movieId", "rating"], 
                            dtype={"userId":int, "movieId":int, "rating":float})
# Construção da estrutura 3
ratings_hash = ListHashTable(45000)
temp_userID = -1
temp_pair_list = list()
for row in ratings_file.itertuples(index=False):
    #ratings_hash.insert(row[0], (row[1], row[2]))
    # sistema para inserir vários ratings por vez
    # fica uns 5 segundos mais rápido no meu computador :)
    if row[0] == temp_userID:
        temp_pair_list.append((row[1], row[2]))
    else:
        if len(temp_pair_list) > 0:
            ratings_hash.bulk_insert(temp_userID, temp_pair_list)
        temp_pair_list = [(row[1], row[2])]
        temp_userID = row[0]

    temp_movie = movies_hash.search(row[1])
    if temp_movie != False:
        temp_movie[4] += row[2]
        temp_movie[5] += 1


for bucket in movies_hash.table:
    for entry in bucket:
        if entry[5] != 0:
            entry[4] = entry[4]/entry[5]

# Leitura de tags.csv
tags_file = pandas.read_csv("./tags.csv", 
                            usecols=["movieId","tag"], 
                            dtype={"movieId":int, "tag":str})
# Construção da estrutura 4
tags_hash = ListHashTable(20000, keytype='str')
for row in tags_file.itertuples(index=False):
    tags_hash.insert(row[1], row[0])


end_time = time.perf_counter()
build_time = (end_time - start_time)*1000
print(build_time)
print("Fim")

# ========================
#   Cemitério dos Testes
# ========================

pesquisa1("America")
    



"""print(title_trie.search("Toy Story"))
print(title_trie.search("Toy Story 2"))
print(title_trie.search("Toy2"))
print(title_trie.search("y"))
print(title_trie.search("American Winter"))
print(title_trie.search("H-Man, The (Bijo to Ekitainingen)"))"""


#print(ratings_hash.search(1))

"""print("Pesquisa 2:")
pesquisa2(54766)
print("Pesquisa 3:")
pesquisa3(20, 'Mystery')
print("Pesquisa 4:")
pesquisa4("feel-good", "predictable")
print("Pesquisa 2:")
pesquisa2(0)
print("Pesquisa 3:")
pesquisa3(20, 'Mstery')
print("Pesquisa 4:")
pesquisa4("feel-god", "prediable")"""

"""pesquisa2(0)
print(1)
pesquisa2(1)
print(2)
pesquisa2(2)"""

#pesquisa3(20, "Myster")

#pesquisa4("feelgood", "feelgod")

#print(movies_hash.search(102107))
#print(movies_hash.search(2858))

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

"""

#print(len(tags_hash.search("tentou sair do clichÃª")) == len(set(tags_hash.search("tentou sair do clichÃª"))))
#print(tags_hash.search("tentou sair do clichÃª"))
#print(tags_hash.search("Mark Waters"))
#print(tags_hash.search("dark hero"))

"""print(genres_hash.search("Comedy"))
print(genres_hash.search("Comed"))
print(genres_hash.search("Action"))"""
"""print("Movies_Hash: Ocupação, tamMax, tamMedio")
print(movies_hash.size)
print(movies_hash.ocupacao())
print(movies_hash.tamMaxLista())
print(movies_hash.tamMedioLista())
print("Ratings_Hash: Ocupação, tamMax, tamMedio")
print(ratings_hash.size)
print(ratings_hash.ocupacao())
print(ratings_hash.tamMaxLista())
print(ratings_hash.tamMedioLista())
print("Tags_Hash: Ocupação, tamMax, tamMedio")
print(tags_hash.size)
print(tags_hash.ocupacao())
print(tags_hash.tamMaxLista())
print(tags_hash.tamMedioLista())
print("Genres_Hash: Ocupação, tamMax, tamMedio")
print(genres_hash.size)
print(genres_hash.ocupacao())
print(genres_hash.tamMaxLista())
print(genres_hash.tamMedioLista())"""
"""for bucket in genres_hash.table:
    for entry in bucket:
        print(entry[0])"""


    

