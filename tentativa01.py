import pandas

### Definição da Tabela Hash
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



### Leitura de movies.csv
movies_file = pandas.read_csv("./movies.csv", 
                              dtype={"movieId":int, "title":str, "genres": str, "year": int})
# Construção da tabela hash
movies_hash = HashTable(3000)
for row in movies_file.itertuples(index=False):
    movie_list = list(i for i in row)
    movie_list.extend([0, 0])
    movies_hash.insert(movie_list)



# Testes
if __name__ == "__main__":
    print(movies_hash.search(1))
    print(movies_hash.search(221))
    print(movies_hash.search(131262))
    
