import tentativa01
import tkinter as tk
from tkinter import ttk

# Verifica se um caractere é um dígito (0 a 9)
def e_digito(c):
    return c >= '0' and c <= '9'

# Converte uma string numérica (como '123') para inteiro
# Retorna -1 se a string tiver qualquer caractere não numérico
def string_para_inteiro(s):
    num = 0
    for c in s:
        if not e_digito(c):
            return -1  # erro: string não numérica
        num = num * 10 + (ord(c) - ord('0'))  # conversão manual de char para número
    return num

# Remove espaços em branco no início e no final da string
def remover_espacos(s):
    inicio = 0
    while inicio < len(s) and s[inicio] == ' ':
        inicio += 1

    fim = len(s) - 1
    while fim >= 0 and s[fim] == ' ':
        fim -= 1

    if inicio > fim:
        return ""  # string vazia (só espaços)
    else:
        resultado = ""
        for i in range(inicio, fim + 1):
            resultado += s[i]
        return resultado

def consultas(comando):

        # Verifica comando que começa com "prefixo "
        if len(comando) >= 8 and comando[:8] == "prefixo ":
            prefixo = remover_espacos(comando[8:])  # remove espaços após o comando
            return tentativa01.pesquisa1(prefixo)

        # Verifica comando que começa com "user "
        elif len(comando) >= 5 and comando[:5] == "user ":
            parte = remover_espacos(comando[5:])
            user_id = string_para_inteiro(parte)
            if user_id != -1:
                return tentativa01.pesquisa2(user_id)
            else:
                return "erro", [[("UserID inválido.")]]

        # Verifica comando que começa com "top" e um número
        elif len(comando) >= 3 and comando[:3] == "top":
            i = 3
            num_str = ""

            # Lê todos os dígitos após "top"
            while i < len(comando) and e_digito(comando[i]):
                num_str += comando[i]
                i += 1

            n = string_para_inteiro(num_str)

            # Lê o gênero dentro das aspas simples
            genero = ""
            while i < len(comando) and comando[i] != "'":
                i += 1  # pula até encontrar a aspa de abertura
            i += 1  # pula a aspa inicial

            while i < len(comando) and comando[i] != "'":
                genero += comando[i]
                i += 1

            if n != -1:
                return tentativa01.pesquisa3(n, genero)
            else:
                return "erro", print("Comando top inválido.")

        # Verifica comando que começa com "tags" e contém duas strings entre aspas
        elif len(comando) >= 4 and comando[:4] == "tags":
            partes = []
            atual = ""
            lendo = False

            # Extrai duas strings entre aspas simples
            for c in comando[4:]:
                if c == "'":
                    lendo = not lendo
                    if not lendo:
                        partes.append(remover_espacos(atual))
                        atual = ""
                elif lendo:
                    atual += c

            if len(partes) == 2:
               return tentativa01.pesquisa4(partes[0], partes[1])
            else:
                return "erro", [[("Formato esperado: tags 'tag1' 'tag2'")]]

        else:
           return "erro", [[("Comando não reconhecido.")]]
def interface():
    janela = tk.Tk()
    janela.title("MovieLens")

    pesquisa = tk.Entry(janela, width=60)
    pesquisa.pack(padx =10, pady=10)

    def ao_clicar():
        comando = remover_espacos(pesquisa.get())
        tipo, resultado = consultas(comando)
        atualizar_tabela(tipo, resultado)

    botao = tk.Button(janela, text="Pesquisar", command=ao_clicar)
    botao.pack(padx=5)

    tabela = ttk.Treeview(janela, show="headings")
    tabela.pack(padx=10, pady=10, fill="both", expand=True)

    def limpar_tabela():
        for col in tabela["columns"]:
            tabela.heading(col, text="")
        tabela.delete(*tabela.get_children())
        tabela["columns"] = []

    def atualizar_tabela(tipo, resultados):
        limpar_tabela()

        if tipo == "prefixo" or tipo == "top" or tipo == "tags":
            colunas = ["movieId", "title", "genres", "year", "rating", "count"]
        elif tipo == "user":
            colunas = ["movieId", "title", "genres", "year", "global rating", "count", "rating"]
        else:
            tabela.insert("", "end", values=(resultados[0],))
            return

        tabela["columns"] = colunas
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, anchor="w", width=100)

        for item in resultados:
            tabela.insert("", "end", values=item)

    janela.mainloop()

if __name__ == "__main__":
    interface()
